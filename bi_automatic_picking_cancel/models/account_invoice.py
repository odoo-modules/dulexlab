# -*- coding: utf-8 -*-
from odoo import models, api, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_cancel(self):
        for invoice in self:
            res = super(AccountInvoice, invoice).action_cancel()
            if (invoice.type in ['out_refund', 'in_refund']) and (invoice.state == 'cancel'):
                pickings = self.env['stock.picking'].search([('inv_id', '=', invoice.id)])
                pickings.action_cancel()
        return
