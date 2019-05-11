# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    technical_reason_id = fields.Many2one('technical.reason', string='Technical Reason')
    failure_reason_id = fields.Many2one('failure.reason', string='Failure Reason')
    maintenance_team_note = fields.Char(string='Maintenance Team Note')
    complete_status = fields.Selection([('completely', 'Completely'), ('partially', 'Partially')],
                                       string='Complete Status')
    maintenance_line_ids = fields.One2many('maintenance.request.line', 'maintenance_id', string='Parts')
    pickings_created = fields.Boolean(string='Pickings Created')
    picking_count = fields.Integer(string="Pickings", compute='compute_maintenance_pickings')

    @api.multi
    def compute_maintenance_pickings(self):
        for request in self:
            request.picking_count = self.env['stock.picking'].sudo().search_count([('maintenance_id', '=', request.id)])

    @api.multi
    def create_maintenance_request_pickings(self):
        for request in self:
            stock_picking_type_id = int(
                self.env['ir.config_parameter'].sudo().get_param('maintenance_stock_picking_type_id'))

            if not stock_picking_type_id:
                raise ValidationError(
                    _('Please configure picking type for maintenance in inventory configurations.'))

            if not request.maintenance_line_ids:
                raise ValidationError(
                    _('Please add parts first to create transfers.'))

            maintenance_lines_dict = {}
            for maintenance_line in request.maintenance_line_ids:
                key_value = str(maintenance_line.location_id.id) + '_' + str(maintenance_line.location_dest_id.id)
                if key_value in maintenance_lines_dict:
                    maintenance_lines_dict[key_value]['maintenance_lines'] += maintenance_line

                elif key_value not in maintenance_lines_dict:
                    maintenance_lines_dict[key_value] = {'maintenance_lines': [maintenance_line]}

            for prepare_picking_line in maintenance_lines_dict:
                picking_vals = {
                    'origin': request.name,
                    'scheduled_date': fields.Datetime.now(),
                    'picking_type_id': stock_picking_type_id,
                    'location_id': maintenance_lines_dict[prepare_picking_line]['maintenance_lines'][0].location_id.id,
                    'location_dest_id': maintenance_lines_dict[prepare_picking_line]['maintenance_lines'][
                        0].location_dest_id.id,
                    'move_type': 'direct',
                    'state': 'draft',
                    'maintenance_id': request.id,
                }
                created_picking_object = self.env['stock.picking'].create(picking_vals)
                for prepare_move_line in maintenance_lines_dict[prepare_picking_line]['maintenance_lines']:
                    created_move_object = self.env['stock.move'].create({
                        'product_id': prepare_move_line.product_id.id,
                        'name': prepare_move_line.product_id.name,
                        'product_uom_qty': prepare_move_line.product_uom_qty,
                        'product_uom': prepare_move_line.product_uom.id,
                        'location_id': prepare_move_line.location_id.id,
                        'location_dest_id': prepare_move_line.location_dest_id.id,
                        'picking_id': created_picking_object.id,
                    })
                created_picking_object.action_confirm()
            request.pickings_created = True
