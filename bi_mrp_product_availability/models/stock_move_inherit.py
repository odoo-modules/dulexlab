# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):
    _inherit = 'stock.move'

    @api.constrains('product_id', 'product_uom_qty', 'raw_material_production_id')
    def check_available_qty_of_product(self):
        for stock_move in self:
            if stock_move.raw_material_production_id:
                location_qty_available = stock_move.product_id.with_context(
                    location=stock_move.raw_material_production_id.location_src_id.id).virtual_available
                if stock_move.product_uom_qty > location_qty_available:
                    raise ValidationError(
                        _('You plan to produce %s %s of %s but you only have %s %s available in %s location.') % \
                        (stock_move.product_uom_qty, stock_move.product_uom.name, stock_move.product_id.name,
                         location_qty_available, stock_move.product_id.uom_id.name,
                         stock_move.raw_material_production_id.location_src_id.display_name))
