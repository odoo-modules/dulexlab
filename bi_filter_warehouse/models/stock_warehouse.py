# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    appear_in_so = fields.Boolean(string="Appear In SO", default=False)
