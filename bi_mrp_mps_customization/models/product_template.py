import itertools

from odoo.addons import decimal_precision as dp

from odoo import api, fields, models, tools, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_capacity = fields.Float(string="Capacity / Month")
