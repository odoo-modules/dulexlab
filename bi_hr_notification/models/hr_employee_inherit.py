# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    id_expiry_date = fields.Date('Identification Expiry Date')
    id_next_notification = fields.Date()