# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class HrContractInherit(models.Model):
    _inherit = 'hr.contract'

    contract_next_notification = fields.Date(copy=False)
