# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'order_id.pricelist_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            if line.product_id.is_bonus is False:
                taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                                product=line.product_id, partner=line.order_id.partner_shipping_id)
                line.update({
                    'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                })
            else:
                line_price_list = line.order_id.pricelist_id
                line_price = line.product_id.original_product.list_price * line.product_uom_qty
                if line_price_list:
                    line_price -= (line_price * line_price_list.phd_disc) / 100
                    if line_price_list.dd_disc != 0:
                        line_price -= (line_price * line_price_list.dd_disc) / 100
                    else:
                        line_price -= (line_price * line_price_list.cd_disc) / 100
                if line.tax_id:
                    line_tax = line.tax_id.amount
                    line_price = line_price * line_tax / 100
                else:
                    line_price = 0
                line.update({
                    'price_tax': line_price,
                    'price_total': line_price,
                    'price_subtotal': 0,
                })
