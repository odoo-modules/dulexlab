# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_bonus = fields.Boolean(string="Is Bonus")
    original_product = fields.Many2one('product.template', string="Original Product")


class ProductProduct(models.Model):
    _inherit = "product.product"

    is_bonus = fields.Boolean(string="Is Bonus", related="product_tmpl_id.is_bonus")
    original_product = fields.Many2one('product.template', string="Original Product",
                                       related="product_tmpl_id.original_product")
