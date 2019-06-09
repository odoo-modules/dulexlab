# -*- coding: utf-8 -*-

import math
import json
from odoo import http, _, fields
from odoo.http import request
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
# from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager

# class website_account(website_account):
class CustomerPortal(CustomerPortal):

#     @http.route()
#     def account(self, **kw):
#         response = super(website_account, self).account(**kw)
#         partner = request.env.user
#         holidays = request.env['hr.leave']
#         holidays_count = holidays.sudo().search_count([
#         ('user_id', 'child_of', [request.env.user.id]),
#           ])
#         response.qcontext.update({
#         'holidays_count': holidays_count,
#         })
#         return response
    
    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user
        holidays = request.env['hr.leave']

        if request.env.user.has_group('odoo_leave_request_portal_employee.group_employee_leave_manager'):
            holidays_count = holidays.sudo().search_count([])
        else:
            holidays_count = holidays.sudo().search_count([
            ('user_id', 'child_of', [request.env.user.id]),
            # ('type','=','remove')
              ])
        values.update({
        'holidays_count': holidays_count,
        })
        return values
    
    @http.route(['/my/leave_request', '/my/leave_request/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_leave_request(self, page=1, sortby=None, **kw):
        if not request.env.user.has_group('odoo_leave_request_portal_employee.group_employee_leave') and not request.env.user.has_group('odoo_leave_request_portal_employee.group_employee_leave_manager'):
            # return request.render("odoo_timesheet_portal_user_employee.not_allowed_leave_request")
            return request.render("odoo_leave_request_portal_employee.not_allowed_leave_request")
        response = super(CustomerPortal, self)
        values = self._prepare_portal_layout_values()
        holidays_obj = http.request.env['hr.leave']

        if request.env.user.has_group('odoo_leave_request_portal_employee.group_employee_leave_manager'):
            domain = []
        else:
            domain = [
                ('user_id', 'child_of', [request.env.user.id]),
                # ('type','=','remove')
            ]

        # count for pager
        holidays_count = http.request.env['hr.leave'].sudo().search_count(domain)
        # pager
        # pager = request.website.pager(
        pager = portal_pager(
            url="/my/leaves",
            total=holidays_count,
            page=page,
            step=self._items_per_page
        )
        sortings = {
            'date': {'label': _('Newest'), 'order': 'date_from desc'},
        }
        
        order = sortings.get(sortby, sortings['date'])['order']
        
        # content according to pager and archive selected
        holidays = holidays_obj.sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        values.update({
            'holidays': holidays,
            'page_name': 'holidays',
            'sortings' : sortings,
            'sortby': sortby,
            'pager': pager,
            'default_url': '/my/holidays',
        })
        return request.render("odoo_leave_request_portal_employee.display_leave_request", values)


    @http.route(['/leave_request_form'], type='http', auth="user", website=True)
    def portal_leave_request_form(self, **kw):
        if not request.env.user.has_group(
                'odoo_leave_request_portal_employee.group_employee_leave') and not request.env.user.has_group(
                'odoo_leave_request_portal_employee.group_employee_leave_manager'):
            return request.render("odoo_leave_request_portal_employee.not_allowed_leave_request")
        values = {}
        leave_types = request.env['hr.leave.type'].sudo().search([])
        employees = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
        values.update({
            'leave_types': leave_types,
            'employees': employees,
            'error_fields': '',
        })
        return request.render("odoo_leave_request_portal_employee.leave_request_submit", values)


    @http.route(['/leave_request_submit/'], type='http', auth="user", website=True)
    def portal_leave_request_submit(self, **kw):
        vals = {}
        if request.params.get('leave_type', False):
            leave_type_id = int(request.params.get('leave_type'))
            vals.update({
                'holiday_status_id': leave_type_id,
            })
        if request.params.get('employee_id', False):
            employee_id = int(request.params.get('employee_id'))
            vals.update({
                'employee_id': employee_id,
            })
        if request.params.get('half_day', False):
            half_day = True
            vals.update({
                'request_unit_half': half_day,
            })
        if request.params.get('description', False):
            description = request.params.get('description')
            vals.update({
                'name': description,
            })


        date_from = request.params.get('date_from')
        vals.update({
            'request_date_from': date_from,
        })
        date_to = request.params.get('date_to')
        vals.update({
            'request_date_to': date_to,
        })


        created_leave = False
        try:
            if date_from > date_to:
                raise UserError(_('The date to should be greater than or equal the date from !'))
            created_leave = request.env['hr.leave'].sudo().create(vals)

            temp_rec = request.env['hr.leave'].sudo().new(vals)
            # temp_rec._onchange_holiday_status_id()
            temp_rec._onchange_request_parameters()
            temp_rec._onchange_request_unit_half()
            temp_rec._onchange_employee_id()
            temp_rec._onchange_leave_dates()
            rec_vals = temp_rec._convert_to_write(temp_rec._cache)
            created_leave.sudo().write(rec_vals)
        except Exception as e:
            if created_leave:
                created_leave.unlink()
            values = {}
            leave_types = request.env['hr.leave.type'].sudo().search([])
            employees = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
            values.update({
                'leave_types': leave_types,
                'employees': employees,
                'error_fields': json.dumps(e.args[0]),
            })
            return request.render("odoo_leave_request_portal_employee.leave_request_submit", values)

        return request.redirect('/my/leave_request')


    @http.route(['/leave_approve'], type='http', auth="user", website=True)
    def portal_approve_leave_request(self, **kw):
        leave_id = request.params.get('id')
        if leave_id:
            holiday = request.env['hr.leave'].sudo().search([('id', '=', int(leave_id))])
            if holiday:
                try:
                    holiday.action_approve()
                except:
                    pass
        return request.redirect('/my/leave_request')


    @http.route(['/leave_refuse'], type='http', auth="user", website=True)
    def portal_refuse_leave_request(self, **kw):
        leave_id = request.params.get('id')
        if leave_id:
            holiday = request.env['hr.leave'].sudo().search([('id', '=', int(leave_id))])
            if holiday:
                try:
                    holiday.action_refuse()
                except:
                    pass
        return request.redirect('/my/leave_request')