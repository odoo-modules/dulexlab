# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class EmployeeOverTime(models.Model):
    _name = 'employee.overtime'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'

    name = fields.Char(string='Description', track_visibility='onchange')
    state = fields.Selection(
        [('draft', 'Draft'), ('approved', 'Approved'), ('confirmed', 'Confirmed'), ('cancel', 'Canceled')],
        default='draft', copy=False, track_visibility='onchange')
    employee_id = fields.Many2one('hr.employee', string='Employee', track_visibility='onchange')
    image_medium = fields.Binary(related='employee_id.image_medium')
    expect_sign_out = fields.Float('Expect Sing out', track_visibility='onchange')
    act_sign_out = fields.Float('Actual Sing out', track_visibility='onchange')
    diff = fields.Float('Difference', compute='calculate_diff_hours', store=True, track_visibility='onchange')
    reason = fields.Selection(
        [('none', 'None'), ('business_need', 'Business Need'), ('no_business_need', 'No Business Need')],
        string="Reason", default='none')

    @api.multi
    @api.depends('expect_sign_out', 'act_sign_out', 'employee_id')
    def calculate_diff_hours(self):
        for val in self:
            val.diff = val.act_sign_out - val.expect_sign_out
