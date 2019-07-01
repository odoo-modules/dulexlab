# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    warehouse_ids = fields.Many2many('stock.warehouse', string='Warehouse')
