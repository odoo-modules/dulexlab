# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountInvoiceInherit(models.Model):
    _inherit = 'account.invoice'

    validate_show_btn = fields.Boolean('', compute='show_custom_validate_btn', store=1)
    custom_validate_show_btn = fields.Boolean('', compute='show_custom_validate_btn', store=1)

    @api.multi
    @api.depends('refund_invoice_id', 'state', 'type')
    def show_custom_validate_btn(self):
        for invoice in self:
            if (not invoice.refund_invoice_id) and (invoice.state == 'draft'):
                invoice.validate_show_btn = True
            else:
                invoice.validate_show_btn = False

            if invoice.refund_invoice_id and (invoice.state == 'draft'):
                invoice.custom_validate_show_btn = True
            else:
                invoice.custom_validate_show_btn = False
