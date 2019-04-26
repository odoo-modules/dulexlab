# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountInvoiceInherit(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        super(AccountInvoiceInherit, self).action_invoice_open()
        for record in self:
            record.create_refund_picking()

    @api.multi
    def create_refund_picking(self):
        for invoice in self:
            if invoice.refund_invoice_id:
                # TODO Picking >> Customer Invoice
                if invoice.refund_invoice_id.type == 'out_invoice':
                    operation_type = 'incoming'
                    location_id_code = 'customer'
                    dest_location_id_code = 'internal'
                    origin = invoice.number

                # TODO Picking >> Vendor Bill Invoice
                if invoice.refund_invoice_id.type == 'in_invoice':
                    operation_type = 'outgoing'
                    location_id_code = 'internal'
                    dest_location_id_code = 'vendor'
                    origin = invoice.number

                picking_type_id = self.env['stock.picking.type'].search([('code', '=', operation_type)], limit=1)
                location_id = self.env['stock.location'].search(
                    [('usage', '=', location_id_code), '|', ('company_id', '=', invoice.company_id.id),
                     ('company_id', '=', False)], limit=1)
                location_dest_id = self.env['stock.location'].search(
                    [('usage', '=', dest_location_id_code), '|', ('company_id', '=', invoice.company_id.id),
                     ('company_id', '=', False)], limit=1)

                stock_picking = self.env['stock.picking'].create({
                    'partner_id': invoice.partner_id.id,
                    'picking_type_id': picking_type_id.id,
                    'company_id': invoice.company_id.id,
                    'location_id': location_id.id,
                    'location_dest_id': location_dest_id.id,
                    'origin': origin,
                })
                for line in invoice.invoice_line_ids:
                    self.env['stock.move'].create({
                        'name': invoice.name,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.quantity,
                        'product_uom': line.uom_id.id or line.product_id.uom_id.id,
                        'location_id': location_id.id,
                        'location_dest_id': location_dest_id.id,
                        'picking_id': stock_picking.id,
                    })
                stock_picking.action_assign()
