# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BillOfMaterials(models.Model):
    _inherit = "mrp.bom"

    cost_structure_location_ids = fields.Many2many('stock.location', string="Locations")

    @api.depends('cost_structure_location_ids')
    @api.multi
    def set_available_qty_in_lines(self):
        for bom in self:
            for line in bom.bom_line_ids:
                line.set_available_qty()


class BillOfMaterialsLine(models.Model):
    _inherit = "mrp.bom.line"

    available_qty = fields.Float(string="Available Qty", compute='set_available_qty')

    @api.depends('bom_id.cost_structure_location_ids')
    @api.multi
    def set_available_qty(self):
        for line in self:
            if line.bom_id:
                bom = line.bom_id
                if bom.cost_structure_location_ids:
                    location_ids = bom.cost_structure_location_ids.ids
                else:
                    location_ids = self.env['stock.location'].search([('usage', '=', 'internal')]).ids
                quants = self.env['stock.quant'].search([
                    ('product_id', '=', line.product_id.id),
                    ('location_id', 'in', location_ids),
                ])
                line.available_qty = sum((quant.quantity - quant.reserved_quantity) for quant in quants)
