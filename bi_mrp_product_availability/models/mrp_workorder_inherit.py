# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    def open_tablet_view(self):
        self.ensure_one()
        for stock_move in self.production_id.move_raw_ids:
            location_qty_available = stock_move.product_id.with_context(
                location=stock_move.raw_material_production_id.location_src_id.id).qty_available
            if stock_move.product_uom.id == stock_move.product_id.uom_id:
                if stock_move.product_uom_qty > location_qty_available:
                    raise ValidationError(
                        _('You plan to produce %s %s of %s but you only have %s %s available in %s location.') % \
                        (stock_move.product_uom_qty, stock_move.product_uom.name, stock_move.product_id.name,
                         location_qty_available, stock_move.product_id.uom_id.name,
                         stock_move.raw_material_production_id.location_src_id.display_name))
            elif stock_move.product_uom.category_id.id == stock_move.product_id.uom_id.category_id.id:
                if stock_move.product_uom_qty > (location_qty_available * stock_move.product_uom.factor):
                    raise ValidationError(
                        _('You plan to produce %s %s of %s but you only have %s %s available in %s location.') % \
                        (stock_move.product_uom_qty, stock_move.product_uom.name, stock_move.product_id.name,
                         location_qty_available, stock_move.product_id.uom_id.name,
                         stock_move.raw_material_production_id.location_src_id.display_name))
        return super(MrpWorkorder, self).open_tablet_view()
