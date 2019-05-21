# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class HrAttendanceInherit(models.Model):
    _inherit = 'hr.attendance'
    overtime_id = fields.Many2one('employee.overtime')
