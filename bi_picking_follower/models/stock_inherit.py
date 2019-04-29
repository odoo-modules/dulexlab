# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def _create_backorder(self, backorder_moves=[]):
        backorders = super(StockPickingInherit, self)._create_backorder()
        for picking in self:
            partners = []
            bos = backorders.filtered(lambda bo: bo.backorder_id == picking)
            if bos and picking.purchase_id and picking.purchase_id.user_id and picking.purchase_id.user_id.partner_id.id not in partners:
                partners.append(picking.purchase_id.user_id.partner_id.id)
                bos.message_subscribe(partner_ids=partners)
        return backorders