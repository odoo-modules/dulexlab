# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
from datetime import datetime


class HrAttendanceInherit(models.Model):
    _inherit = 'hr.attendance'

    @api.model
    def create(self, values):
        res = super(HrAttendanceInherit, self).create(values)
        overtime_obj = self.env['employee.overtime']
        employee_obj = res['employee_id']
        check_out = res['check_out']
        if check_out:
            check_out = datetime.strptime(str(check_out), "%Y-%m-%d %H:%M:%S")  # convert into datetime format
            time_checkout = datetime.strftime(check_out, "%H:%M")  # convert into string format and extract time only

            # Todo Working schedule line
            for wsl in employee_obj.contract_id.resource_calendar_id.attendance_ids:
                wsl_day_name = dict(wsl._fields['dayofweek'].selection).get(wsl.dayofweek)  # get value selection field
                if wsl_day_name == check_out.strftime("%A"):
                    print('ok name')
                    if time_checkout > str(wsl.hour_to):
                        print('ok bigger')
                        t, s = time_checkout.split(":")
                        vals = {'employee_id': employee_obj.id,
                                'reason': 'none',
                                'expect_sign_out': wsl.hour_to,
                                'act_sign_out': float(t) + (float(s) / 60)}
                        overtime_obj.sudo().create(vals)
            # raise ValidationError(_())

        return res
