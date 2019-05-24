# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT



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
            time_checkout = datetime.strftime(check_out, "%H:%M")  # convert into string format and extract time only

            # Todo Working schedule line
            for wsl in employee_obj.contract_id.resource_calendar_id.attendance_ids:
                wsl_day_name = dict(wsl._fields['dayofweek'].selection).get(wsl.dayofweek)  # get value selection field
                if wsl_day_name == check_out.strftime("%A"):
                    if time_checkout > str(wsl.hour_to):
                        t, s = time_checkout.split(":")

                        vals = {'employee_id': employee_obj.id,
                                'reason': 'none',
                                'expect_sign_out': round(wsl.hour_to,2),
                                'attend_id': res.id,
                                'act_sign_out': round(float(t) + (float(s) / 60),2)}
                        overtime_obj.sudo().create(vals)

        return res
