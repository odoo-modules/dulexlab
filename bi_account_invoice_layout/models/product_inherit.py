# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ProductTempInherit(models.Model):
    _inherit = 'product.template'

    public_price_lst = fields.Monetary(string='Public Price', compute='get_public_price_lst')

    @api.depends('list_price')
    def get_public_price_lst(self):
        for product in self:
            prod_public_price_rate = self.env['ir.config_parameter'].sudo().get_param('prod_public_price_rate')
            product.public_price_lst = product.list_price * float(prod_public_price_rate)
