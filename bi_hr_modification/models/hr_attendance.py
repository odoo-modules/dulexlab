# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

import pytz


class HrAttendanceInherit(models.Model):
    _inherit = 'hr.attendance'

    @api.model
    def create(self, values):
        res = super(HrAttendanceInherit, self).create(values)
        overtime_obj = self.env['employee.overtime']
        employee_obj = res['employee_id']
        check_out = res['check_out']

        if check_out:
            check_out = datetime.strptime(str(check_out), DATETIME_FORMAT)  # convert into datetime format
            attend_checkout_date = fields.Datetime.from_string(res.check_out)

            user = self.env['res.users'].search([('id', '=', self.env.uid)])

            user_time_zone = pytz.timezone(user.partner_id.tz) or pytz.utc
            user_time_zone_offset = datetime.now(user_time_zone).utcoffset().total_seconds() / 60 / 60
            check_out_hours = (attend_checkout_date + timedelta(hours=user_time_zone_offset)).strftime('%H:%M')

            # Todo Working schedule line
            for wsl in employee_obj.contract_id.resource_calendar_id.attendance_ids:
                wsl_day_name = dict(wsl._fields['dayofweek'].selection).get(wsl.dayofweek)  # get value selection field
                if wsl_day_name == check_out.strftime("%A"):
                    if check_out_hours > str(wsl.hour_to):
                        t, s = check_out_hours.split(":")
                        vals = {'employee_id': employee_obj.id,
                                'reason': 'none',
                                'expect_sign_out': round(wsl.hour_to, 2),
                                'attend_id': res.id,
                                'overtime_type': 'working_days',
                                'act_sign_out': round(float(t) + (float(s) / 60), 2)}
                        overtime_obj.sudo().create(vals)

            # Todo NOT Working schedule line !!!
            working_days = []
            for day in employee_obj.contract_id.resource_calendar_id.attendance_ids:
                day_name = dict(wsl._fields['dayofweek'].selection).get(day.dayofweek)
                if day_name not in working_days:
                    working_days.append(day_name)

            if check_out.strftime("%A") not in working_days:
                check_in = fields.Datetime.from_string(res.check_in)
                check_out = fields.Datetime.from_string(res.check_out)
                difference = relativedelta(check_out, check_in)
                days = difference.days
                hours = (days * 24) + difference.hours
                minutes = difference.minutes

                vals = {'employee_id': employee_obj.id,
                        'reason': 'none',
                        'expect_sign_out': False,
                        'attend_id': res.id,
                        'overtime_type': 'days_off',
                        'act_sign_out': round(float(hours) + (float(minutes) / 60), 2)}
                overtime_obj.sudo().create(vals)

        return res
