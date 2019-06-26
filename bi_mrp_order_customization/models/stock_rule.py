from odoo import api, fields, models, _


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _prepare_mo_vals(self, product_id, product_qty, product_uom, location_id, name, origin, values, bom):
        res = super(StockRule, self)._prepare_mo_vals(product_id, product_qty, product_uom, location_id, name, origin, values, bom)
        mrp = self.env['mrp.production'].search([('name', '=', origin)], limit=1)
        print(origin)
        if mrp:
            res['parent_mo_id'] = mrp.id
        return res
