# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
                 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
                 'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.quantity, product=self.product_id,
                                                          partner=self.invoice_id.partner_id)
        if self.product_id.is_bonus is False:
            self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else self.quantity * price
            self.price_total = taxes['total_included'] if taxes else self.price_subtotal
        else:
            line_tax = 0.0
            line_price_list = self.invoice_id.partner_id.property_product_pricelist
            if self.invoice_line_tax_ids:
                line_tax = self.invoice_line_tax_ids[0].amount
            self.price_total = (self.product_id.original_product.list_price * self.quantity * line_tax) / 100
            if line_price_list:
                self.price_total -= (self.price_total * line_price_list.phd_disc) / 100
                if line_price_list.dd_disc != 0:
                    self.price_total -= (self.price_total * line_price_list.dd_disc) / 100
                else:
                    self.price_total -= (self.price_total * line_price_list.cd_disc) / 100
            self.price_subtotal = price_subtotal_signed = 0
            self.price_tax = 0

        if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            currency = self.invoice_id.currency_id
            date = self.invoice_id._get_currency_rate_date()
            price_subtotal_signed = currency._convert(price_subtotal_signed, self.invoice_id.company_id.currency_id,
                                                      self.company_id or self.env.user.company_id,
                                                      date or fields.Date.today())
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign
