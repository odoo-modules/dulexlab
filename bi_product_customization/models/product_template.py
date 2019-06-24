# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_color = fields.Char(string="Color")
    effective_date = fields.Date(string="Effective Date")
    validity_period = fields.Integer(string="Validity Period (Months)")
    packaging_desc = fields.Char(string="Packaging Desc.")
