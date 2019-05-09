# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    maintenance_stock_picking_type_id = fields.Many2one('stock.picking.type', string='Picking Type',
                                                        domain=[('code', '=', 'internal')])

    def set_values(self):
        set_param = self.env['ir.config_parameter'].set_param
        set_param('maintenance_stock_picking_type_id', (self.maintenance_stock_picking_type_id.id))
        super(ResConfigSettings, self).set_values()

    @api.multi
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        maintenance_stock_picking_type_id = self.env['ir.config_parameter'].sudo().get_param(
            'maintenance_stock_picking_type_id')
        if maintenance_stock_picking_type_id:
            res.update(
                maintenance_stock_picking_type_id=int(maintenance_stock_picking_type_id),
            )
        return res
