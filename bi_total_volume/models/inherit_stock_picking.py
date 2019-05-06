# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    total_vol_for_init_demand = fields.Float(string="Total Volume For Initial Demand", compute='_compute_amount',
                                             readonly=True)
    total_vol_for_done = fields.Float(string="Total Volume For Done Qty", compute='_compute_amount', readonly=True)

    @api.multi
    @api.depends('move_ids_without_package')
    def _compute_amount(self):
        for rec in self:
            qty = 0.0
            qty_done = 0.0
            if rec.move_ids_without_package:
                for line in rec.move_ids_without_package:
                    qty += line.product_uom_qty * line.product_id.volume
                    qty_done += line.quantity_done * line.product_id.volume
            rec.total_vol_for_init_demand = qty
            rec.total_vol_for_done = qty_done