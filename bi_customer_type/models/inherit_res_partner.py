# -*- coding: utf-8 -*-
from odoo import models, fields, api


class InheritResPartner(models.Model):
    _inherit = 'res.partner'

    customer_type = fields.Many2one('customer.type', string="Partner Type")