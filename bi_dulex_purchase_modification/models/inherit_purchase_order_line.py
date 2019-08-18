# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    remaining_qty = fields.Float(string="Remaining Qty", stored=True, compute='_onchange_qty')

    @api.onchange('product_qty', 'qty_received')
    def _onchange_qty(self):
        for line in self:
            line.remaining_qty = line.product_qty - line.qty_received