# -*- coding: utf-8 -*-

import math

from odoo import http, _, fields
from odoo.http import request
from datetime import datetime, timedelta
from odoo.exceptions import UserError
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


    @http.route(['/leave_approve'], type='http', auth="user", website=True)
    def portal_approve_leave_request(self, **kw):
        leave_id = request.params.get('id')
        if leave_id:
            holiday = request.env['hr.leave'].sudo().search([('id', '=', int(leave_id))])
            if holiday:
                holiday.action_approve()
        return request.redirect('/my/leave_request')