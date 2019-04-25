# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.constrains('product_id', 'product_uom_qty')
    def check_available_qty_of_product(self):
        for line in self:
            location_qty_available = line.product_id.with_context(
                location=line.order_id.warehouse_id.out_type_id.default_location_src_id.id).virtual_available
            if line.product_uom_qty > location_qty_available:
                raise ValidationError(
                    _('You plan to sell %s %s of %s but you only have %s %s available in %s location.') % \
                    (line.product_uom_qty, line.product_uom.name, line.product_id.name,
                     location_qty_available, line.product_id.uom_id.name,
                     line.order_id.warehouse_id.out_type_id.default_location_src_id.display_name))
