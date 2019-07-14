# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AccountInvoiceRefund(models.TransientModel):
    _inherit = "account.invoice.refund"

    @api.multi
    def compute_refund(self, mode='refund'):
        res = super(AccountInvoiceRefund, self).compute_refund(mode='refund')
        active_id = self.env.context.get('active_ids', [])
        for refund in self:
            created_invoice_id = res['domain'][1][2]
            if created_invoice_id:
                created_invoice = self.env['account.invoice'].browse(created_invoice_id)
                active_invoice = self.env['account.invoice'].browse(active_id)
                if created_invoice:
                    created_invoice.write({'pricelist_id': active_invoice.pricelist_id.id})
        return res