# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    def get_default_picking_type(self):
        maintenance_stock_picking_type_id = int(
            self.env['ir.config_parameter'].sudo().get_param('maintenance_stock_picking_type_id'))
        if maintenance_stock_picking_type_id:
            return maintenance_stock_picking_type_id

    technical_reason_id = fields.Many2one('technical.reason', string='Technical Reason')
    failure_reason_id = fields.Many2one('failure.reason', string='Failure Reason')
    maintenance_team_note = fields.Char(string='Maintenance Team Note')
    complete_status = fields.Selection([('completely', 'Completely'), ('partially', 'Partially')],
                                       string='Complete Status')

    maintenance_line_ids = fields.One2many('maintenance.request.line', 'maintenance_id', string='Parts')

    stock_picking_type_id = fields.Many2one('stock.picking.type', string='Picking Type', required=True,
                                            domain=[('code', '=', 'internal')], default=get_default_picking_type)
