# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        product_dict = {}
        self.ensure_one()
        for line in self.order_line:
            if line.product_id.type == 'product' and line.product_id.id in product_dict:
                product_dict[line.product_id.id]['line_qty'] += line.product_uom_qty
            elif line.product_id.type == 'product' and line.product_id.id not in product_dict:
                product_dict[line.product_id.id] = {'line_product': line.product_id, 'line_qty': line.product_uom_qty}

        for product in product_dict:
            location_onhand_qty = product_dict[product]['line_product'].with_context(
                location=self.warehouse_id.out_type_id.default_location_src_id.id).qty_available

            location_outgoing_qty = product_dict[product]['line_product'].with_context(
                location=self.warehouse_id.out_type_id.default_location_src_id.id).outgoing_qty

            location_qty_available = location_onhand_qty - location_outgoing_qty
            if product_dict[product]['line_qty'] > location_qty_available:
                raise ValidationError(
                    _('You plan to sell %s %s of %s but you only have %s %s available in %s location.') % \
                    (product_dict[product]['line_qty'], product_dict[product]['line_product'].uom_id.name,
                     product_dict[product]['line_product'].name,
                     location_qty_available, product_dict[product]['line_product'].uom_id.name,
                     self.warehouse_id.out_type_id.default_location_src_id.display_name))
        return super(SaleOrder, self).action_confirm()
