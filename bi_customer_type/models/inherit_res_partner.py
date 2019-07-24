# -*- coding: utf-8 -*-
from odoo import models, fields, api


class InheritResPartner(models.Model):
    _inherit = 'res.partner'

    customer_type = fields.Many2one('customer.type', string="Partner Type")
    customer_category_id = fields.Many2one('partner.category', string="Partner Category",
                                           related="customer_type.category_id", store=True)

    @api.onchange('customer_type')
    def set_customer_category(self):
        for partner in self:
            partner.customer_category_id = partner.customer_type.category_id
