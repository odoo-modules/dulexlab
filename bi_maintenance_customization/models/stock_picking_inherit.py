# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    maintenance_id = fields.Many2one(
        'maintenance.request', string='Maintenance Reference')
