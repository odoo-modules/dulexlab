# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def get_taxes_values(self):
        tax_grouped = {}
        round_curr = self.currency_id.round
        for line in self.invoice_line_ids:
            if not line.account_id:
                continue
            price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            if self.type in ['out_refund', 'out_invoice']:
                if line.product_id.is_bonus is True:
                    taxes = \
                        line.invoice_line_tax_ids.compute_all(line.product_id.original_product.lst_price, self.currency_id,
                                                              line.quantity,
                                                              line.product_id.original_product,
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
                            if self.partner_id.property_product_pricelist:
                                tax['amount'] -= tax['amount'] * (self.partner_id.property_product_pricelist.phd_disc / 100)
                                if self.partner_id.property_product_pricelist.dd_disc != 0:
                                    tax['amount'] -= tax['amount'] * (self.partner_id.property_product_pricelist.dd_disc / 100)
                                else:
                                    tax['amount'] -= tax['amount'] * (self.partner_id.property_product_pricelist.cd_disc / 100)

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
            if self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.cd_disc > 0.0:
                self.sudo().write({'ks_global_discount_rate': self.partner_id.property_product_pricelist.cd_disc})

        return tax_grouped
