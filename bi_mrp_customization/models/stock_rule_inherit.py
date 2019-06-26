# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _prepare_mo_vals(self, product_id, product_qty, product_uom, location_id, name, origin, values, bom):
        if self._context.get('order_partner', False) and origin:
            origin += '/%s' % self._context.get('order_partner')
        vals = super(StockRule, self)._prepare_mo_vals(product_id, product_qty, product_uom, location_id, name, origin, values, bom)
        return vals