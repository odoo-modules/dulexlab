# -*- coding: utf-8 -*-

import math
import json
from odoo import http, _, fields
from odoo.http import request
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_round
# from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager

import math
from pytz import timezone, UTC
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
from odoo.tools import float_compare, DEFAULT_SERVER_DATE_FORMAT


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
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
        holidays = request.env['hr.leave']

        if request.env.user.has_group('odoo_leave_request_portal_employee.group_employee_leave_manager'):
            employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
            if employee:
                holidays_count = holidays.sudo().search_count(['|', ('user_id', 'child_of', [request.env.user.id]),
                          ('employee_id.parent_id', '=', employee.id)])
            else:
                holidays_count = holidays.sudo().search_count([])
        else:
            holidays_count = holidays.sudo().search_count([
            ('user_id', 'child_of', [request.env.user.id]),
            # ('type','=','remove')
              ])

        values.update({
            'holidays_count': holidays_count,
            'employee_data': employee,
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

        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)

        if request.env.user.has_group('odoo_leave_request_portal_employee.group_employee_leave_manager'):
            domain = []
            if employee:
                domain = ['|', '|', ('user_id', 'child_of', [request.env.user.id]), ('employee_id.parent_id', '=', employee.id), ('employee_id', '=', employee.id)]
        else:
            if employee:
                domain = [
                    '|',
                    ('user_id', 'child_of', [request.env.user.id]),
                    ('employee_id', '=', employee.id)
                ]
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
            url="/my/leave_request",
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
        holidays_balance = {}
        for holiday in holidays:
            if holiday.holiday_status_id.allocation_type != 'no':
                holidays_balance[holiday.id] = _('%g remaining out of %g') % (float_round(holiday.holiday_status_id.with_context(employee_id=holiday.employee_id.id).remaining_leaves, precision_digits=2) or 0.0, float_round(holiday.holiday_status_id.with_context(employee_id=holiday.employee_id.id).max_leaves, precision_digits=2) or 0.0)
            else:
                holidays_balance[holiday.id] = _('No allocation')
        values.update({
            'holidays': holidays,
            'holidays_balance': holidays_balance,
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



    ###################################
    ###  leaves validations/onchanges
    ###################################

    def _check_date(self, vals):
        if vals.get('date_from', False) and vals.get('date_to', False) and vals.get('employee_id', False):
            domain = [
                ('date_from', '<=', vals.get('date_to')),
                ('date_to', '>', vals.get('date_from')),
                ('employee_id', '=', vals.get('employee_id')),
                ('state', 'not in', ['cancel', 'refuse']),
            ]
            nholidays = request.env['hr.leave'].sudo().search_count(domain)
            if nholidays:
                raise ValidationError(_('You can not have 2 leaves that overlaps on the same day.'))

    def _check_holidays(self, vals):
        holiday_status_id = vals.get('holiday_status_id', False)
        if holiday_status_id:
            holiday_status_id = request.env['hr.leave.type'].sudo().browse([holiday_status_id])
            if vals.get('employee_id', False) and holiday_status_id and holiday_status_id.allocation_type != 'no':
                leave_days = holiday_status_id.get_days(vals.get('employee_id'))[holiday_status_id.id]
                if float_compare(leave_days['remaining_leaves'], 0, precision_digits=2) == -1 or \
                                float_compare(leave_days['virtual_remaining_leaves'], 0, precision_digits=2) == -1:
                    raise ValidationError(_('The number of remaining leaves is not sufficient for this leave type.\n'
                                            'Please also check the leaves waiting for validation.'))

    def _check_leave_type_validity(self, vals):
        if vals.get('holiday_status_id', False):
            holiday_status_id = request.env['hr.leave.type'].sudo().browse([vals.get('holiday_status_id')])
            if holiday_status_id.validity_start and holiday_status_id.validity_stop:
                vstart = holiday_status_id.validity_start
                vstop = holiday_status_id.validity_stop
                dfrom = vals.get('date_from', False)
                dto = vals.get('date_to', False)
                if dfrom and dto and (dfrom.date() < vstart or dto.date() > vstop):
                    raise UserError(
                        _('You can take %s only between %s and %s') % (
                            holiday_status_id.display_name, holiday_status_id.validity_start,
                            holiday_status_id.validity_stop))
        else:
            raise UserError(_('Please select leave type'))


    def _onchange_request_parameters(self, vals):
        if not vals.get('request_date_from', False):
            vals.update({'date_from': False})
            return vals

        if vals.get('request_unit_half', False):
            vals.update({'request_date_to': vals.get('request_date_from')})

        if not vals.get('request_date_to', False):
            vals.update({'date_to': False})
            return vals

        employee_id = False
        if vals.get('employee_id', False):
            employee_id = request.env['hr.employee'].sudo().browse([vals.get('employee_id')])

        resource_calendar_id = employee_id.resource_calendar_id.id if employee_id else request.env.user.company_id.resource_calendar_id.id

        domain = [('calendar_id', '=', resource_calendar_id)]
        attendances = request.env['resource.calendar.attendance'].sudo().search(domain, order='dayofweek, day_period DESC')

        # find first attendance coming after first_day
        attendance_from = next((att for att in attendances if int(att.dayofweek) >= vals.get('request_date_from').weekday()), attendances[0])
        # find last attendance coming before last_day
        attendance_to = next((att for att in reversed(attendances) if int(att.dayofweek) <= vals.get('request_date_to').weekday()), attendances[-1])

        if vals.get('request_unit_half', False):
            hour_from = float_to_time(attendance_from.hour_from)
            hour_to = float_to_time(attendance_from.hour_to)
        else:
            hour_from = float_to_time(attendance_from.hour_from)
            hour_to = float_to_time(attendance_to.hour_to)

        tz = request.env.user.tz if request.env.user.tz else 'UTC'  # custom -> already in UTC
        date_from = timezone(tz).localize(datetime.combine(vals.get('request_date_from'), hour_from)).astimezone(UTC).replace(tzinfo=None)
        date_to = timezone(tz).localize(datetime.combine(vals.get('request_date_to'), hour_to)).astimezone(UTC).replace(tzinfo=None)
        vals.update({'date_from': date_from})
        vals.update({'date_to': date_to})

        return vals

    def _onchange_request_unit_half(self, vals):
        if vals.get('request_unit_half', False):
            vals.update({
                'request_unit_hours': False,
                'request_unit_custom': False
            })
        vals = self._onchange_request_parameters(vals)
        return vals

    def _onchange_employee_id(self, vals):
        if vals.get('employee_id', False):
            employee_id = request.env['hr.employee'].sudo().browse([vals.get('employee_id')])
            if employee_id:
                vals.update({
                    'manager_id': employee_id.parent_id.id if employee_id.parent_id else False,
                    'department_id': employee_id.department_id.id
                })
        return vals

    def _get_number_of_days(self, date_from, date_to, employee_id):
        """ Returns a float equals to the timedelta between two dates given as string."""
        if employee_id:
            employee = request.env['hr.employee'].browse(employee_id)
            return employee.sudo().get_work_days_data(date_from, date_to)['days']

        time_delta = date_to - date_from
        return math.ceil(time_delta.days + float(time_delta.seconds) / 86400)

    def _onchange_leave_dates(self, vals):
        if vals.get('date_from', False) and vals.get('date_to', False):
            number_of_days = self._get_number_of_days(vals.get('date_from'), vals.get('date_to'), vals.get('employee_id', False))
        else:
            number_of_days = 0
        vals.update({
            'number_of_days': number_of_days,
        })
        return vals


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
            'request_date_from': datetime.strptime(date_from, DEFAULT_SERVER_DATE_FORMAT) if date_from else False,
        })
        date_to = request.params.get('date_to')
        vals.update({
            'request_date_to': datetime.strptime(date_to, DEFAULT_SERVER_DATE_FORMAT) if date_to else False,
        })


        created_leave = False
        try:
            vals = self._onchange_request_parameters(vals)
            vals = self._onchange_request_unit_half(vals)
            vals = self._onchange_employee_id(vals)
            vals = self._onchange_leave_dates(vals)

            self._check_date(vals)
            self._check_holidays(vals)
            self._check_leave_type_validity(vals)

            created_leave = request.env['hr.leave'].sudo().create(vals)

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
                    holiday.write({
                        'report_note': request.params.get('description') if request.params.get('description') else False
                    })
                except:
                    pass
        return request.redirect('/my/leave_request')