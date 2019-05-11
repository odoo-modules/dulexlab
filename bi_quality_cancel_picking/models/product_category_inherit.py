# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class ProductCategoryInherit(models.Model):
    _inherit = 'product.category'

    quality_control = fields.Boolean(string='Quality Control?', help='this will cancel stock moves of failed quality checks')