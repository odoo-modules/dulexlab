# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountAssets(models.Model):
    _inherit = 'account.asset.asset'

    value_residual = fields.Float(compute='_amount_residual', method=True, digits=0, string='Residual Value', store=True)
    accu_depreciation = fields.Float(string="Accumulated Depreciation", compute="_total_depreciation", store=True)