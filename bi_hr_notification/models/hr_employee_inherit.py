# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
from datetime import time as d_time
from pytz import timezone, utc
import time
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
from collections import namedtuple
import ast


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    id_expiry_date = fields.Date('Identification Expiry Date')
    id_next_notification = fields.Date(copy=False)
    emp_code = fields.Char('Code')

    linked_absence = fields.Integer('Linked Absence')
    unlinked_absence = fields.Integer('Un-linked Absence')


    def get_weekends(self, date_from, date_to, work_days, resource_calendar_id):
        week_days = [0, 1, 2, 3, 4, 5, 6]  # ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        schedule_days = []
        for line in resource_calendar_id.attendance_ids:
            schedule_days.append(int(line.dayofweek))
        schedule_days = list(set(schedule_days))
        weekend_days = list(set(week_days) - set(schedule_days))

        count = 0
        if work_days > len(schedule_days) or (date_from.weekday() not in weekend_days and date_from.weekday()):
            delta = timedelta(days=1)
            while date_from <= date_to:
                if date_from.weekday() in weekend_days:
                    count += 1
                date_from += delta

        return count

    @api.model
    def attendance_notification(self):
        linked_table_header = "<table style='width: 100%;padding:10px;'><tbody><tr><td style='width:33%;padding:10px;border:1px solid gray'>Employee Name</td><td style='width:33%;padding:10px;border:1px solid gray'>Employee Code</td><td style='width:33%;padding:10px;border:1px solid gray'>Last Check Out From</td></tr>"
        linked_table_data = ''

        unlinked_table_header = "<table style='width: 100%;padding:10px;'><tbody><tr><td style='width:33%;padding:10px;border:1px solid gray'>Employee Name</td><td style='width:33%;padding:10px;border:1px solid gray'>Employee Code</td><td style='width:33%;padding:10px;border:1px solid gray'>Un-linked Absence days</td></tr>"
        unlinked_table_data = ''

        table_end = '</tbody></table>'

        recipient_ids = []
        absence_days_groups_ids = ast.literal_eval(
            (self.env['ir.config_parameter'].sudo().get_param('absence_days_groups_ids')))
        for group in self.env['res.groups'].search([('id', 'in', absence_days_groups_ids)]):
            for user in group.users:
                if user.partner_id.id not in recipient_ids:
                    recipient_ids.append(user.partner_id.id)

        get_param = self.env['ir.config_parameter'].sudo().get_param
        unlinked_days = int(get_param('unlinked_days'))
        linked_days = int(get_param('linked_days'))

        for employee in self.search([]):
            today_date = date.today()
            year_from = date.today().replace(day=1, month=1)
            year_datetime_from = datetime.combine(datetime.now().replace(day=1, month=1), d_time.min)

            # ----------------- recipients ------------------#
            # if employee.parent_id.address_home_id.id and (employee.parent_id.address_home_id.id not in recipient_ids):
            #     recipient_ids.append(employee.parent_id.address_home_id.id)

            # Todo Linked Absence
            if linked_days and employee.resource_calendar_id:
                attendance_obj = self.env['hr.attendance'].search([('employee_id', '=', employee.id),
                                                                   ('check_in', '!=', False),
                                                                   ('check_in', '>=', year_from),
                                                                   ('check_in', '<', today_date)],
                                                                  order='check_in desc', limit=1)
                if attendance_obj:
                    if attendance_obj.check_out:
                        last_check_out = attendance_obj.check_out + timedelta(days=1)
                    else:
                        last_check_out = attendance_obj.check_in + timedelta(days=1)
                else:
                    last_check_out = year_datetime_from

                d_frm_obj = last_check_out
                d_to_obj = datetime.now()

                tzinfo = employee.resource_calendar_id.tz
                d_frm_obj = timezone(tzinfo).localize(d_frm_obj) if tzinfo else d_frm_obj
                d_to_obj = timezone(tzinfo).localize(d_to_obj) if tzinfo else d_to_obj

                work_data = employee.get_work_days_data(d_frm_obj, d_to_obj, calendar=employee.resource_calendar_id, compute_leaves=True)
                no_days = work_data['days']

                weekends_no = self.get_weekends(d_frm_obj.date(), d_to_obj.date(), no_days, employee.resource_calendar_id)
                no_days = work_data['days'] + weekends_no

                if linked_days and (no_days >= linked_days):

                    linked_table_data += "<tr><td style='width:33%;padding:10px;border:1px solid gray'>" + employee.name + "</td><td style='width:33%;padding:10px;border:1px solid gray'>" + str(
                        employee.emp_code or ' ') + "</td><td style='width:33%;padding:10px;border:1px solid gray'>" + str(
                        no_days) + "/days</td></tr>"

            # Todo Un-Linked Absence
            if unlinked_days:
                days = 0
                start_date = date.today().replace(day=1, month=1)
                increment_date = start_date
                day_lst = []
                unlinked = 0
                for attendance in employee.resource_calendar_id.attendance_ids:
                    if dict(attendance._fields['dayofweek'].selection).get(attendance.dayofweek) not in day_lst:
                        day_lst.append(dict(attendance._fields['dayofweek'].selection).get(attendance.dayofweek))

                while (increment_date >= start_date) and (increment_date <= today_date):
                    increment_date = start_date + relativedelta(days=+days)
                    days += 1
                    increment_check_out = start_date + relativedelta(days=+days)

                    if increment_date.strftime("%A") in day_lst:
                        emp_att_obj = self.env['hr.attendance'].search([('employee_id', '=', employee.id),
                                                                        ('check_in', '>=', increment_date),
                                                                        ('check_in', '<', increment_check_out),
                                                                        ], order='check_out desc')
                        check_leaves = employee.check_leaves(employee_id=employee.id, check_from=increment_date,
                                                             check_to=increment_check_out)
                        if not emp_att_obj and not check_leaves:
                            unlinked += 1

                if unlinked >= unlinked_days:
                    unlinked_table_data += "<tr><td style='width:33%;padding:10px;border:1px solid gray'>" + employee.name + "</td><td style='width:33%;padding:10px;border:1px solid gray'>" + str(
                        employee.emp_code or ' ') + "</td><td style='width:33%;padding:10px;border:1px solid gray'>" + str(
                        unlinked) + "/days</td></tr>"

        if recipient_ids:
            if linked_table_data:
                mail_data = {'subject': 'linked absence mail notification',
                             'body_html': 'Dears' + ',<br/>' + linked_table_header + linked_table_data + table_end,
                             'recipient_ids': [(6, 0, recipient_ids)],
                             'author_id': self.env.ref('base.partner_admin').id,
                             }
                mail = self.env['mail.mail'].create(mail_data)
                mail.send()

            if unlinked_table_data:
                mail_data = {'subject': 'Un-linked absence mail notification',
                             'body_html': 'Dears' + ',<br/>' + unlinked_table_header + unlinked_table_data + table_end,
                             'recipient_ids': [(6, 0, recipient_ids)],
                             'author_id': self.env.ref('base.partner_admin').id,
                             }
                mail = self.env['mail.mail'].create(mail_data)
                mail.send()

    @api.multi
    def check_leaves(self, employee_id, check_from, check_to):
        if employee_id and check_to and check_from:
            leave_list = []
            Range = namedtuple('Range', ['start', 'end'])
            leave_objs = self.env['hr.leave'].search(
                [('state', '=', 'validate'), ('employee_id', '=', employee_id),
                 ('holiday_status_id.request_unit', '=', 'day'), ], order='request_date_from desc')
            for leave in leave_objs:
                r1 = Range(start=leave.date_from.date(), end=leave.date_to.date())
                r2 = Range(start=check_from, end=check_to)
                latest_start = max(r1.start, r2.start)
                earliest_end = min(r1.end, r2.end)
                delta = (earliest_end - latest_start).days
                overlap = max(0, delta)
                if overlap and (leave not in leave_list):
                    leave_list.append(leave)
            return leave_list
