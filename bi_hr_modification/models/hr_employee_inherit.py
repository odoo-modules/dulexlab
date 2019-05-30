# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    last_accumulate_date = fields.Date('Last Accumulate Date')
