# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')

    @api.onchange('pricelist_id')
    def get_ks_global_discount_rate(self):
        for invoice in self:
            invoice.ks_global_discount_rate = invoice.pricelist_id.cd_disc
            for line in invoice.invoice_line_ids:
                line._compute_price()

    @api.onchange('partner_id')
    def get_default_invoice_pricelist(self):
        for invoice in self:
            if invoice.type == 'out_refund':
                invoice.pricelist_id = invoice.partner_id.property_product_pricelist.id

    @api.multi
    def recompute_lines_prices(self):
        for invoice in self:
            for line in invoice.invoice_line_ids:
                line._compute_price()

    @api.multi
    def get_taxes_values(self):
        tax_grouped = {}
        round_curr = self.currency_id.round
        for line in self.invoice_line_ids:
            if not line.account_id:
                continue
            price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            if self.type in ['out_refund', 'out_invoice'] and line.product_id:
                if line.product_id.is_bonus:
                    taxes = \
                        line.invoice_line_tax_ids.compute_all(line.product_id.original_product.lst_price,
                                                              self.currency_id,
                                                              line.quantity,
                                                              line.product_id,
                                                              self.partner_id)['taxes']
                else:
                    taxes = \
                        line.invoice_line_tax_ids.compute_all(line.product_id.lst_price, self.currency_id,
                                                              line.quantity,
                                                              line.product_id,
                                                              self.partner_id)['taxes']

                for line_tax in line.invoice_line_tax_ids:
                    for tax in taxes:
                        if tax['name'] == line_tax.name:
                            if self.pricelist_id:
                                tax['amount'] -= tax['amount'] * (
                                        self.pricelist_id.phd_disc / 100)
                                tax['amount'] -= tax['amount'] * (
                                        self.pricelist_id.dd_disc / 100)

            else:
                taxes = \
                    line.invoice_line_tax_ids.compute_all(price_unit, self.currency_id, line.quantity, line.product_id,
                                                          self.partner_id)['taxes']

            for tax in taxes:
                val = self._prepare_tax_line_vals(line, tax)
                key = self.env['account.tax'].browse(tax['id']).get_grouping_key(val)

                if key not in tax_grouped:
                    tax_grouped[key] = val
                    tax_grouped[key]['base'] = round_curr(val['base'])
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base'] += round_curr(val['base'])
        if self.type == 'out_refund':
            if self.pricelist_id and self.pricelist_id.cd_disc > 0.0:
                self.sudo().write({'ks_global_discount_rate': self.pricelist_id.cd_disc})

        return tax_grouped
