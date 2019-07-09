# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    def get_component_lot(self):
        active_id = self.env.context.get('active_id')
        active_workorder = self.env['mrp.workorder'].browse(active_id)
        product_lot_objects = self.env['stock.production.lot'].search(
            [('product_id', '=', active_workorder.component_id.id), ('product_qty', '>', 0)])
        product_lot_ids = [lot.id for lot in product_lot_objects if lot.product_qty > 0]
        return [('id', 'in', product_lot_ids)]

    lot_id = fields.Many2one('stock.production.lot', readonly=False, related=False, compute='get_component_lot_value', )

    # domain=get_component_lot)

    @api.depends('component_id')
    def get_component_lot_value(self):
        for work_order in self:
            product_lots = self.env['stock.production.lot'].search(
                [('product_id', '=', work_order.component_id.id)])
            product_move = work_order.move_raw_ids.filtered(
                lambda stock_move: stock_move.product_id == work_order.component_id)
            move_product_lot_ids = product_move.move_line_ids.mapped('lot_id')
            if move_product_lot_ids:
                work_order.lot_id = move_product_lot_ids[0]
            else:
                product_lot_objects = self.env['stock.production.lot'].search(
                    [('product_id', '=', work_order.component_id.id), ('product_qty', '>', 0)])
                product_lot_ids = [lot.id for lot in product_lot_objects if lot.product_qty > 0]
                if product_lot_ids:
                    work_order.lot_id = product_lot_ids[0]
