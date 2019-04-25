# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def _create_picking(self):
        res = super(PurchaseOrderInherit, self)._create_picking()
        for order in self:
            if any([ptype in ['product', 'consu'] for ptype in order.order_line.mapped('product_id.type')]):
                pickings = order.picking_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
                if pickings and order.user_id:
                    pickings.message_subscribe(partner_ids=order.user_id.partner_id.ids)
        return res