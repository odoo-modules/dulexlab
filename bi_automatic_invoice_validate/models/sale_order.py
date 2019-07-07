# -*- coding: utf-8 -*-
from odoo import models, api, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_invoice_create(self, grouped=False, final=False):
        invoices = super(SaleOrder, self).action_invoice_create(grouped, final)
        for invoice_id in invoices:
            invoice = self.env['account.invoice'].browse(invoice_id)
            invoice.action_invoice_open()
        return invoices
