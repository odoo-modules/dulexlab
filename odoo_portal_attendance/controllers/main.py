# -*- coding: utf-8 -*-

import datetime
import calendar
import time

from odoo import http, _
from odoo.http import request
# from datetime import datetime, timedelta
from datetime import date 
from odoo import models, fields, registry, SUPERUSER_ID
# from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.exceptions import UserError

class MyAttendance(http.Controller):
    
    @http.route(['/my/sign_in_attendance'], type='http', auth="user", website=True)
    def sign_in_attendace(self, **post):
        if not request.env.user.has_group('odoo_portal_attendance.portal_user_employee_attendance'):
            return request.render("odoo_portal_attendance.not_allowed_attendance")
        import datetime
        employee = request.env['hr.employee'].search([('user_id', '=', request.env.user.id)])
        check_in = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if employee:
            vals = {
                    'employee_id': employee.id,
                    'check_in': check_in,
                    'check_in_web':True,
                    }
            attendance = request.env['hr.attendance'].sudo().create(vals)
            values = {
                    'attendance':attendance
                }
        # return request.render('odoo_portal_attendance.sign_in_attendance', values)
            return request.render('odoo_portal_attendance.sign_in_attendance', values)

    @http.route(['/my/sign_out_attendance'], type='http', auth="user", website=True)
    def sign_out_attendace(self, **post):
        if not request.env.user.has_group('odoo_portal_attendance.portal_user_employee_attendance'):
            return request.render("odoo_portal_attendance.not_allowed_attendance")
        import datetime
        employee = request.env['hr.employee'].search([('user_id', '=', request.env.user.id)])
        
        no_check_out_attendances = request.env['hr.attendance'].search([
                    ('employee_id', '=', employee.id),
                    ('check_out', '=', False),
                ])
        check_out = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        attendance = no_check_out_attendances.write({'check_out':check_out})
        values = {
                    'attendance':attendance
                }
        return request.render('odoo_portal_attendance.sign_out_attendance')

# class website_account(website_account):
class CustomerPortal(CustomerPortal):
    
    @http.route()
    def account(self, **kw):
        import datetime
        response = super(CustomerPortal, self).account(**kw)
        employee = request.env['hr.employee'].search([('user_id', '=', request.env.user.id)])
        attendance_obj = request.env['hr.attendance']
        
        attendance_count = attendance_obj.sudo().search_count(
            [('employee_id','=', employee.id),
             ])
        response.qcontext.update({
                'attendance_count': attendance_count,
        })
        return response
    
    def _prepare_portal_layout_values(self):
        import datetime
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        employee = request.env['hr.employee'].search([('user_id', '=', request.env.user.id)], limit=1)
        attendance_obj = request.env['hr.attendance']

        now = datetime.datetime.now()
        year = now.year
        month = now.month
        num_days = calendar.monthrange(year, month)[1]
        month_days = [datetime.date(year, month, day) for day in range(1, num_days + 1)]

        attendance_count = 0
        attendance_recs = {}
        if employee:
            attendance_count = attendance_obj.sudo().search_count(
                [('employee_id','=', employee.id),
                 ])
            attendances = attendance_obj.sudo().search([
                ('employee_id', '=', employee.id),
                ('check_in_date', 'in', month_days),
             ])
            for att in attendances:
                if att.check_in_date:
                    attendance_recs[att.check_in_date] = att

        values.update({
            'attendance_count': attendance_count,
            'attendance_recs': attendance_recs,
            'month_days': month_days,
            'now_date': now.date(),
        })
        return values
    
    @http.route(['/my/attendances', '/my/attendances/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_attendances(self, page=1, sortby=None, **kw):
        if not request.env.user.has_group('odoo_portal_attendance.portal_user_employee_attendance'):
            return request.render("odoo_portal_attendance.not_allowed_attendance")
        import datetime
        response = super(CustomerPortal, self)
        values = self._prepare_portal_layout_values()
        employee = request.env['hr.employee'].search([('user_id', '=', request.env.user.id)])
        attendance_obj = http.request.env['hr.attendance']
        
        domain = [
            ('employee_id', '=', employee.id),
        ]
        # count for pager
        attendance_count = attendance_obj.sudo().search_count(domain)
        
        # pager
        # pager = request.website.pager(
        pager = portal_pager(
            url="/my/attendances",
            total=attendance_count,
            page=page,
            step=self._items_per_page
        )
        
        no_check_out_attendances = request.env['hr.attendance'].sudo().search([
                     ('employee_id', '=', employee.id),
                     ('check_out', '=', False),
                 ])
        
        # content according to pager and archive selected
        
        attendances = attendance_obj.sudo().search(domain, limit=self._items_per_page, offset=pager['offset'])
        values.update({
            'attendances': attendances,
            'no_check_out_attendances': no_check_out_attendances,
            'page_name': 'attendance',
            'pager': pager,
            'default_url': '/my/attendances',
        })
        return request.render("odoo_portal_attendance.display_attendances", values)
