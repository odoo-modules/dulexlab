# -*- coding: utf-8 -*-
from odoo import models, fields, api


class InheritMrpBom(models.Model):
    _inherit = 'mrp.bom'

    total_qty = fields.Float(compute='_compute_total_qty', string='Total Qty')

    @api.multi
    @api.depends('bom_line_ids')
    def _compute_total_qty(self):
        for rec in self:
            qty = 0.0
            if rec.bom_line_ids:
                for line in rec.bom_line_ids:
                    # if not line.is_delivery:
                        qty += line.product_qty
        rec.total_qty = qty
