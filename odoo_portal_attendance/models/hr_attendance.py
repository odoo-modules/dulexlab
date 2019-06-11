# -*- coding: utf-8 -*-

from odoo import models, fields, api

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
            rec.check_in_date = rec.check_in.date()