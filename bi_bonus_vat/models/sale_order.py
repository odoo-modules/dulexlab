# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    vat_with_bonus = fields.Monetary(string='VAT', store=True, readonly=True, compute="get_vat_with_bonus", track_visibility='always')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='get_vat_with_bonus', track_visibility='always', track_sequence=6)

    @api.depends('order_line.price_total')
    @api.multi
    def get_vat_with_bonus(self):
        for record in self:
            total_bonus_vat = 0.0
            for line in record.order_line:
                if line.product_id.is_bonus:
                    print(line.product_uom_qty, line.product_id.original_product.list_price, line.tax_id.amount)
                    total_bonus_vat += (line.product_uom_qty *
                                        line.product_id.original_product.list_price * line.tax_id.amount) / 100
            record._amount_all()
            record.vat_with_bonus = total_bonus_vat + record.amount_tax
            record.amount_total = record.amount_untaxed + record.vat_with_bonus
