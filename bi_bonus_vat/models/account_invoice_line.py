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
        invoice_price_list = self.invoice_id.pricelist_id
        if self.product_id.is_bonus:
            self.price_total = (self.product_id.original_product.lst_price)
            if self.invoice_line_tax_ids:
                total_tax_amount = sum([tax_line.amount for tax_line in self.invoice_line_tax_ids])
                self.price_total = (self.product_id.original_product.lst_price * self.quantity) * (
                        total_tax_amount / 100)

            if invoice_price_list:
                self.price_total -= self.price_total * (invoice_price_list.phd_disc / 100)
                self.price_total -= self.price_total * (invoice_price_list.dd_disc / 100)
            self.price_subtotal = price_subtotal_signed = 0
            self.price_tax = 0

        if self.invoice_id and self.invoice_id.pricelist_id and not self.invoice_id.refund_invoice_id and self.invoice_id.type == 'out_refund':
            if invoice_price_list:
                self.price_subtotal -= (self.price_subtotal * (invoice_price_list.phd_disc / 100))
                self.price_subtotal -= (self.price_subtotal * (invoice_price_list.dd_disc / 100))
                self.price_total = self.price_subtotal

                if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
                    currency = self.invoice_id.currency_id
                    date = self.invoice_id._get_currency_rate_date()
                    price_subtotal_signed = currency._convert(self.price_subtotal,
                                                              self.invoice_id.company_id.currency_id,
                                                              self.company_id or self.env.user.company_id,
                                                              date or fields.Date.today())
                    sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
                    self.price_subtotal_signed = price_subtotal_signed * sign

        return res
