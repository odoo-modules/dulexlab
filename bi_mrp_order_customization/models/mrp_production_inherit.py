# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    parent_mo_id = fields.Many2one('mrp.production', string="Parent MO")
    def _log_downside_manufactured_quantity(self, moves_modification):

        def _keys_in_sorted(move):
            """ sort by picking and the responsible for the product the
            move.
            """
            return (move.picking_id.id, move.product_id.responsible_id.id)

        def _keys_in_groupby(move):
            """ group by picking and the responsible for the product the
            move.
            """
            return (move.picking_id, move.product_id.responsible_id)

        def _render_note_exception_quantity_mo(rendering_context):
            values = {
                'production_order': self,
                'order_exceptions': dict((key, d[key]) for d in rendering_context for key in d),
                'impacted_pickings': False,
                'cancel': False
            }
            return self.env.ref('mrp.exception_on_mo').render(values=values)

        documents = {}
        for move, (old_qty, new_qty) in moves_modification.items():
            document = self.env['stock.picking']._log_activity_get_documents(
                {move: (old_qty, new_qty)}, 'move_dest_ids', 'DOWN', _keys_in_sorted, _keys_in_groupby)
            for key, value in document.items():
                if documents.get(key):
                    documents[key] += [value]
                else:
                    documents[key] = [value]
        print(documents)
        self.env['stock.picking']._log_activity(_render_note_exception_quantity_mo, documents)

    def _log_manufacture_exception(self, documents, cancel=False):

        def _render_note_exception_quantity_mo(rendering_context):
            visited_objects = []
            order_exceptions = {}
            for exception in rendering_context:
                order_exception, visited = exception
                order_exceptions.update(order_exception)
                visited_objects += visited
            visited_objects = self.env[visited_objects[0]._name].concat(*visited_objects)
            impacted_object = []
            if visited_objects and visited_objects._name == 'stock.move':
                visited_objects |= visited_objects.mapped('move_orig_ids')
                impacted_object = visited_objects.filtered(lambda m: m.state not in ('done', 'cancel')).mapped('picking_id')
            values = {
                'production_order': self,
                'order_exceptions': order_exceptions,
                'impacted_object': impacted_object,
                'cancel': cancel
            }
            return self.env.ref('mrp.exception_on_mo').render(values=values)
        print(documents)
        self.env['stock.picking']._log_activity(_render_note_exception_quantity_mo, documents)
