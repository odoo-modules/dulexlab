# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sum_of_products = fields.Float(string="Total Order Volume", compute='_compute_total_sum')

    @api.multi
    @api.depends('order_line')
    def _compute_total_sum(self):
        for rec in self:
            qty = 0.0
            if rec.order_line:
                for line in rec.order_line:
                    qty += line.product_uom_qty * line.volume
            rec.sum_of_products = qty


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    volume = fields.Float(string="Volume", store=True, related='product_id.volume', readonly=True)
