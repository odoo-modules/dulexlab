# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('pricelist_id')
    def set_pricelist_orderlines(self):
        for order in self:
            for line in order.order_line:
                line._compute_amount()
                line._onchange_discount()

    @api.multi
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        for order in self:
            res['pricelist_id'] = order.pricelist_id.id
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        res = super(SaleOrderLine, self)._compute_amount()
        for line in self:
            if line.product_id.is_bonus:
                line_price = line.product_id.original_product.list_price * line.product_uom_qty
                if line.order_id.pricelist_id.dd_disc:
                    line_price -= line_price * (line.order_id.pricelist_id.dd_disc / 100)
                if line.order_id.pricelist_id.phd_disc:
                    line_price -= line_price * (line.order_id.pricelist_id.phd_disc / 100)
                if line.tax_id:
                    line_total_tax_amount = sum([tax_line.amount for tax_line in line.tax_id])
                    line_price = line_price * (line_total_tax_amount / 100)
                else:
                    line_price = 0

                line.update({
                    'price_tax': line_price,
                    'price_total': line_price,
                    'price_subtotal': 0,
                })
        return res
