# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
                 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
                 'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        res = super(AccountInvoiceLine, self)._compute_price()
        if self.product_id.is_bonus:
            partner_price_list = self.invoice_id.partner_id.property_product_pricelist
            self.price_total = (self.product_id.original_product.lst_price)
            if self.invoice_line_tax_ids:
                total_tax_amount = sum([tax_line.amount for tax_line in self.invoice_line_tax_ids])
                self.price_total = (self.product_id.original_product.lst_price * self.quantity) * (
                        total_tax_amount / 100)

            if partner_price_list:
                self.price_total -= self.price_total * (partner_price_list.phd_disc / 100)
                self.price_total -= self.price_total * (partner_price_list.dd_disc / 100)
            self.price_subtotal = price_subtotal_signed = 0
            self.price_tax = 0
        return res
