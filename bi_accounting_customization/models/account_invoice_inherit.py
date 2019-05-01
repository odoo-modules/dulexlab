# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountInvoiceInherit(models.Model):
    _inherit = 'account.invoice'

    validate_show_btn = fields.Boolean('', compute='show_custom_validate_btn', store=1)
    custom_validate_show_btn = fields.Boolean('', compute='show_custom_validate_btn', store=1)
    pickings_count = fields.Integer(compute='get_pickings_count')

    @api.multi
    def get_pickings_count(self):
        for invoice in self:
            picking_objs = self.env['stock.picking'].search([('inv_id', '=', invoice.id)])
            invoice.pickings_count = len(picking_objs)

    @api.multi
    def get_pickings(self):
        return {'domain': "[('inv_id', '=', %s)]" % self.id,
                'name': _("Pickings"),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'stock.picking',
                'type': 'ir.actions.act_window'}

    @api.multi
    @api.depends('refund_invoice_id', 'state', 'type')
    def show_custom_validate_btn(self):
        for invoice in self:
            if (invoice.type in ['out_invoice', 'in_invoice']) and (invoice.state == 'draft'):
                invoice.validate_show_btn = True
            else:
                invoice.validate_show_btn = False
                invoice.custom_validate_show_btn = True
