# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class InvoiceValidateWizard(models.TransientModel):
    _name = 'invoice.validate.wizard'

    invoice_id = fields.Many2one('account.invoice', string='Invoice', )
    location_id = fields.Many2one('stock.location', string='Location', )
    location_dest_id = fields.Many2one('stock.location', string='Destination Location', )
    operation_type_id = fields.Many2one('stock.picking.type', string='Picking Type', )

    @api.onchange('invoice_id')
    def get_fields_domain(self):
        self.location_id = False
        self.location_dest_id = False
        self.operation_type_id = False
        active_id = self.env.context.get('active_id')
        inv_id = self.env['account.invoice'].search([('id', '=', active_id)])
        operation_type_ids = []
        location_ids = []
        location_dest_ids = []

        # TODO Picking >> Customer Invoice
        if inv_id.refund_invoice_id.type == 'out_invoice':
            print('customer')
            operation_type_ids = self.env['stock.picking.type'].search(
                [('code', '=', 'incoming'), ('warehouse_id.company_id', '=', self.invoice_id.company_id.id)])
            location_ids = self.env['stock.location'].search(
                [('usage', '=', 'customer'), '|', ('company_id', '=', self.invoice_id.company_id.id),
                 ('company_id', '=', False)])
            location_dest_ids = self.env['stock.location'].search(
                [('usage', '=', 'internal'), '|', ('company_id', '=', self.invoice_id.company_id.id),
                 ('company_id', '=', False)])

            if len(location_ids):
                self.location_id = location_ids.ids[0]

        # TODO Picking >> Vendor Bill Invoice
        if self.invoice_id.refund_invoice_id.type == 'in_invoice':
            print(' vendor')
            operation_type_ids = self.env['stock.picking.type'].search(
                [('code', '=', 'incoming'), ('warehouse_id.company_id', '=', self.invoice_id.company_id.id)],
                order='id')
            location_ids = self.env['stock.location'].search(
                [('usage', '=', 'internal'), '|', ('company_id', '=', self.invoice_id.company_id.id),
                 ('company_id', '=', False)])
            location_dest_ids = self.env['stock.location'].search(
                [('usage', '=', 'supplier'), '|', ('company_id', '=', self.invoice_id.company_id.id),
                 ('company_id', '=', False)])

        if len(operation_type_ids):
            self.operation_type_id = operation_type_ids.ids[0]

        return {
            'domain': {'location_id': [('id', 'in', location_ids.ids if len(location_ids) else [])],
                       'location_dest_id': [('id', 'in', location_dest_ids.ids if len(location_dest_ids) else [])],
                       'operation_type_id': [('id', 'in', operation_type_ids.ids if len(operation_type_ids) else [])],
                       }}

    @api.multi
    def create_refund_picking(self):
        active_id = self.env.context.get('active_id')
        inv_id = self.env['account.invoice'].search([('id', '=', active_id)])
        inv_id.action_invoice_open()
        origin = inv_id.number
        stock_picking = self.env['stock.picking'].create({
            'partner_id': inv_id.partner_id.id,
            'picking_type_id': self.operation_type_id.id,
            'company_id': inv_id.company_id.id,
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id,
            'origin': origin,
        })
        for line in inv_id.invoice_line_ids:
            self.env['stock.move'].sudo().create({
                'name': origin,
                'state': 'draft',
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'product_uom': line.uom_id.id or line.product_id.uom_id.id,
                'location_id': self.location_id.id,
                'location_dest_id': self.location_dest_id.id,
                'picking_id': stock_picking.id,
            })
        stock_picking.action_assign()
