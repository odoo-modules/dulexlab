# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'


class SaleOrderLLineInherit(models.Model):
    _inherit = 'sale.order.line'
