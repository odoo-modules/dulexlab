# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision as dp


class MaintenanceRequestLine(models.Model):
    _name = 'maintenance.request.line'

    def get_default_source_location(self):
        maintenance_stock_picking_type_id = int(
            self.env['ir.config_parameter'].sudo().get_param('maintenance_stock_picking_type_id'))
        picking_type_object = self.env['stock.picking.type'].search([('id', '=', maintenance_stock_picking_type_id)])
        if picking_type_object:
            return picking_type_object.default_location_src_id

    def get_default_dest_location(self):
        maintenance_stock_picking_type_id = int(
            self.env['ir.config_parameter'].sudo().get_param('maintenance_stock_picking_type_id'))
        picking_type_object = self.env['stock.picking.type'].search([('id', '=', maintenance_stock_picking_type_id)])
        if picking_type_object:
            return picking_type_object.default_location_dest_id

    name = fields.Text('Description', required=True)
    maintenance_id = fields.Many2one(
        'maintenance.request', 'Maintenance Reference', ondelete='cascade')

    product_id = fields.Many2one('product.product', 'Product', required=True)
    product_uom_qty = fields.Float(
        'Quantity', default=1.0,
        digits=dp.get_precision('Product Unit of Measure'), required=True)
    product_uom = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        required=True)
    location_id = fields.Many2one(
        'stock.location', 'Source Location', default=get_default_source_location,
        required=True)
    location_dest_id = fields.Many2one(
        'stock.location', 'Dest. Location', default=get_default_dest_location,
        required=True)
    lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial')

    @api.constrains('lot_id', 'product_id')
    def constrain_lot_id(self):
        for line in self.filtered(lambda x: x.product_id.tracking != 'none' and not x.lot_id):
            raise ValidationError(
                _("Serial number is required for operation line with product '%s'") % (line.product_id.name))

    @api.onchange('product_id', 'product_uom_qty')
    def onchange_product_id(self):
        if not self.product_id or not self.product_uom_qty:
            return
        if self.product_id:
            self.name = self.product_id.display_name
            if self.product_id.description_sale:
                self.name += '\n' + self.product_id.description_sale
            self.product_uom = self.product_id.uom_id.id
