# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    tag_id = fields.Many2many('res.partner.category', string="Tags", stored=True, related='partner_id.category_id')