# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CustomerType(models.Model):
    _name = 'customer.type'

    name = fields.Char(string="Partner Type")
    category_id = fields.Many2one('partner.category', string="Partner Category", required=True)
