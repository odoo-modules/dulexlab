# -*- coding: utf-8 -*-
from odoo import models, fields, api


class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_type = fields.Many2one('customer.type', string="Customer Type", related='partner_id.customer_type', store=True) #, related='partner_id.customer_type'
    assigned = fields.Boolean(compute="_get_customer_type", string="Assigned")

    @api.one
    @api.depends('partner_id')
    def _get_customer_type(self):

        if self.customer_type:

            self.assigned = True

        else:

            self.customer_type = False