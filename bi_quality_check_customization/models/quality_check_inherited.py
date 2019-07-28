# -*- coding: utf-8 -*-
from odoo import models, fields, api


class InheritedQualityCheck(models.Model):
    _inherit = 'quality.check'

    move_id = fields.Many2one('stock.move', compute="get_picking_data")
    move_line_ids = fields.One2many('stock.move.line', 'quality_check_id', related="move_id.move_line_ids")
    partner_id = fields.Many2one('res.partner', string="Partner", related='picking_id.partner_id')
    initial_demand = fields.Float(string="Initial Demand", related='move_id.product_uom_qty')
    done_qty = fields.Float(string="Qty Done", related='move_id.quantity_done')
    uom_qty = fields.Many2one('uom.uom', string="Unit Of Measure", related='move_id.product_uom')

    @api.multi
    def get_picking_data(self):
        for point in self:
            flag = False
            for move in point.picking_id.move_ids_without_package:
                if point.product_id == move.product_id and move.product_id:
                    point.move_id = move.id
                    point.move_line_ids = move.move_line_ids.ids
                    flag = True
            if not flag:
                point.move_id = False
                point.move_line_ids = False


class InheritedStockMove(models.Model):
    _inherit = 'stock.move'

    quality_check_id = fields.One2many('quality.check', 'move_id')


class InheritedStockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    quality_check_id = fields.Many2one('quality.check')
