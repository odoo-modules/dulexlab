# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    taxable_order = fields.Boolean(string='Taxable')

    @api.onchange('taxable_order')
    def change_line_taxes(self):
        for order in self:
            if order.taxable_order:
                tax_ids = self.env['account.tax'].search([('type_tax_use', '=', 'sale'), ('taxable', '=', True)])
                if tax_ids and order.order_line:
                    for line in order.order_line:
                        line.tax_id = tax_ids.ids


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    tax_id = fields.Many2many('account.tax', string='Taxes', default=False,
                              domain=['|', ('active', '=', False), ('active', '=', True)])

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        result = super(SaleOrderLine, self).product_id_change()
        for line in self:
            if line.order_id.taxable_order:
                tax_ids = self.env['account.tax'].search([('type_tax_use', '=', 'sale'), ('taxable', '=', True)])
                if tax_ids:
                    line.tax_id = tax_ids.ids
        return result
