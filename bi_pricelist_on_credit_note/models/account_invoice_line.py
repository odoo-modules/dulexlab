# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    # ('out_refund', 'Customer Credit Note'),
    # ('in_refund', 'Vendor Credit Note'),

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
                 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
                 'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        super(AccountInvoiceLine, self)._compute_price()
        if self.invoice_id and self.invoice_id.type in ['out_refund']:
            pricelist = self.partner_id.property_product_pricelist
            self.price_subtotal = price_subtotal_signed = self.price_subtotal - (
                    self.price_subtotal * (pricelist.phd_disc / 100) +
                    self.price_subtotal * (pricelist.dd_disc / 100) +
                    self.price_subtotal * (pricelist.cd_disc / 100)
            )
            self.price_total = self.price_total - (
                    self.price_total * (pricelist.phd_disc / 100) +
                    self.price_total * (pricelist.dd_disc / 100) +
                    self.price_total * (pricelist.cd_disc / 100)
            )
            if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
                currency = self.invoice_id.currency_id
                date = self.invoice_id._get_currency_rate_date()
                price_subtotal_signed = currency._convert(price_subtotal_signed, self.invoice_id.company_id.currency_id,
                                                          self.company_id or self.env.user.company_id,
                                                          date or fields.Date.today())
            sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
            self.price_subtotal_signed = price_subtotal_signed * sign
