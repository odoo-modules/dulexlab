# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.model
    def _compute_default_routing(self):
        for production in self:
            if production.bom_id.routing_id.operation_ids:
                production.routing_id = production.bom_id.routing_id.id
            else:
                production.routing_id = False

    routing_id = fields.Many2one(
        'mrp.routing', string='Routing', default=_compute_default_routing,
        help="The list of operations (list of work centers) to produce the finished product. The routing "
             "is mainly used to compute work center costs during operations and to plan future loads on "
             "work centers based on production planning.")

    inventory_posted = fields.Boolean('Inventory posted', default=False)

    bom_id = fields.Many2one(
        'mrp.bom', 'Bill of Material', track_visibility='onchange',
        readonly=True, states={'confirmed': [('readonly', False)]},
        help="Bill of Materials allow you to define the list of required raw materials to make a finished product.")

    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Operation Type', track_visibility='onchange',
        default=lambda self: self._get_default_picking_type(), required=True)

    @api.multi
    def post_inventory(self):
        res = super(MrpProduction, self).post_inventory()
        for order in self:
            order.inventory_posted = True
        return res

    @api.onchange('bom_id')
    def change_route(self):
        for production in self:
            if production.bom_id.routing_id.operation_ids:
                production.routing_id = production.bom_id.routing_id.id
            else:
                production.routing_id = False

    @api.multi
    def write(self, values):
        res = super(MrpProduction, self).write(values)
        for order in self:
            if 'bom_id' in values or 'picking_type_id' in values:
                self.move_raw_ids._action_cancel()
                self.move_finished_ids._action_cancel()
                self.move_raw_ids.unlink()
                self.move_finished_ids.unlink()
                self.picking_ids.action_cancel()
                self._generate_moves()

            elif 'product_qty' in values and 'bom_id' not in values and 'picking_type_id' not in values:
                for picking in order.picking_ids:
                    for move in picking.move_ids_without_package:
                        # finished product
                        if move.product_id == order.product_id:
                            if order.bom_id.product_qty == 1:
                                move.write({'product_uom_qty': values['product_qty']})
                            elif order.bom_id.product_qty > 1:
                                move.write({'product_uom_qty': values['product_qty'] / order.bom_id.product_qty})
                        # component
                        for bom_line in order.bom_id.bom_line_ids:
                            if bom_line.product_id == move.product_id:
                                if order.bom_id.product_qty == 1:
                                    move.write({'product_uom_qty': values['product_qty'] * bom_line.product_qty})
                                elif order.bom_id.product_qty > 1:
                                    move.write({'product_uom_qty': (values[
                                                                        'product_qty'] * bom_line.product_qty) / order.bom_id.product_qty})

        return res

    def _workorders_create(self, bom, bom_data):
        res = super(MrpProduction, self)._workorders_create(bom, bom_data)
        if self.routing_id.operation_ids:
            res.update({'workcenter_id': self.routing_id.operation_ids[0].workcenter_id.id})
        return res
