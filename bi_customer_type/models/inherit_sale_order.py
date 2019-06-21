# -*- coding: utf-8 -*-
from odoo import models, fields, api


class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_type = fields.Many2one('customer.type', string="Customer Type", related='partner_id.customer_type')
