# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_color = fields.Char(string="Color", related="product_tmpl_id.product_color")
    effective_date = fields.Date(string="Effective Date", related="product_tmpl_id.effective_date")
    validity_period = fields.Integer(string="Validity Period (Months)", related="product_tmpl_id.validity_period")
    packaging_desc = fields.Char(string="Packaging Desc.", related="product_tmpl_id.packaging_desc")
