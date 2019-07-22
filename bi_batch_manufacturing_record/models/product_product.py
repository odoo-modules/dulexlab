# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    batch_sequence = fields.Integer(string="Batch Number", related="product_tmpl_id.batch_sequence")
    batch_step = fields.Integer(string="Batch Step", related="product_tmpl_id.batch_step")
    batch_month = fields.Integer(string="Batch Change Date", related="product_tmpl_id.batch_month")
