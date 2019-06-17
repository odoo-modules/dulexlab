# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pytz

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    
    check_in_web = fields.Boolean(
        'Check In Web',
        default=False, 
        copy=True, 
        required=False
    )

    check_in_date = fields.Date(compute='_get_checkin_date')

    @api.multi
    @api.depends('check_in')
    def _get_checkin_date(self):
        for rec in self:
            if rec.employee_id and rec.employee_id.user_id:
                employee_tz = pytz.timezone(rec.employee_id.user_id.tz or self.sudo().env.user.tz  or 'UTC')
            else:
                employee_tz = pytz.timezone(self.sudo().env.user.tz or 'UTC')
            dt = pytz.UTC.localize(rec.check_in).astimezone(employee_tz).replace(tzinfo=None)
            rec.check_in_date = dt.date()