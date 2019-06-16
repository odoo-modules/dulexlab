# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class CancelReasons(models.Model):
    _name = 'cancel.reason'
    name = fields.Char(string="Cancellation Reason")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    reason_id = fields.Many2one('cancel.reason', track_visibility='always')

    @api.multi
    def action_cancel_with_reason(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cancel Reason',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'quotation.cancel.reason',
            'context': {'sale_order_id': self.id}
        }
