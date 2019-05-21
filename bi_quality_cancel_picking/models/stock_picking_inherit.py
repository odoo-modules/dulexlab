# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    quality_picking_check = fields.Boolean(string='Quality Picking Created?', copy=False)

    def _check_backorder(self):
        """ This method will loop over all the move lines of self and
        check if creating a backorder is necessary. This method is
        called during button_validate if the user has already processed
        some quantities and in the immediate transfer wizard that is
        displayed if the user has not processed any quantities.

        :return: True if a backorder is necessary else False
        """
        quantity_todo = {}
        quantity_done = {}
        # remove failed quality checks moves
        for move in self.mapped('move_lines').filtered(lambda x: x.quality_check_status != 'fail'):
            quantity_todo.setdefault(move.product_id.id, 0)
            quantity_done.setdefault(move.product_id.id, 0)
            quantity_todo[move.product_id.id] += move.product_uom_qty
            quantity_done[move.product_id.id] += move.quantity_done
        for ops in self.mapped('move_line_ids').filtered(lambda x: x.package_id and not x.product_id and not x.move_id):
            for quant in ops.package_id.quant_ids:
                quantity_done.setdefault(quant.product_id.id, 0)
                quantity_done[quant.product_id.id] += quant.qty
        for pack in self.mapped('move_line_ids').filtered(lambda x: x.product_id and not x.move_id):
            quantity_done.setdefault(pack.product_id.id, 0)
            quantity_done[pack.product_id.id] += pack.product_uom_id._compute_quantity(pack.qty_done,
                                                                                       pack.product_id.uom_id)
        return any(quantity_done[x] < quantity_todo.get(x, 0) for x in quantity_done)

    @api.multi
    def create_backorder_quality(self, backorder_moves=[]):
        """ Move all non-done lines into a new backorder picking.
        """
        backorders = self.env['stock.picking']
        for picking in self:
            new_moves_to_backorder = self.env['stock.move']
            moves_to_backorder = picking.move_lines.filtered(
                lambda x: x.state == 'cancel' and x.quality_check_status == 'fail')
            for move in moves_to_backorder:
                new_moves_to_backorder += move.copy()
            if new_moves_to_backorder:
                backorder_picking = picking.copy({
                    'name': '/',
                    'move_lines': [],
                    'move_line_ids': [],
                    'backorder_id': picking.id
                })
                picking.message_post(
                    body=_(
                        'The backorder <a href=# data-oe-model=stock.picking data-oe-id=%d>%s</a> has been created.') % (
                             backorder_picking.id, backorder_picking.name))
                new_moves_to_backorder.write({'picking_id': backorder_picking.id, 'quality_check_status': 'pass'})
                new_moves_to_backorder.mapped('package_level_id').write({'picking_id': backorder_picking.id})
                new_moves_to_backorder.mapped('move_line_ids').write({'picking_id': backorder_picking.id})
                backorder_picking.action_assign()
                backorders |= backorder_picking
            picking.quality_picking_check = True
        return backorders
