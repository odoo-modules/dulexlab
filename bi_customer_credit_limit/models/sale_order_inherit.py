# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        self.ensure_one()
        if self.partner_id.use_credit_limit:
            if self.partner_id.credit_limit_amount:
                partner_allowed_credit_limit_amount = self.partner_id.allowed_amount
                partner_open_invoices = self.env['account.invoice'].search(
                    [('partner_id', '=', self.partner_id.id), ('state', '=', 'open')])
                total_partner_due_amount = sum(invoice.residual for invoice in partner_open_invoices)
                if partner_allowed_credit_limit_amount < (total_partner_due_amount + self.amount_total):
                    raise ValidationError(_('Customer %s exceed his credit limit amount %s %s.' % (
                        self.partner_id.name, self.partner_id.allowed_amount, self.currency_id.symbol)))

            if self.partner_id.credit_limit_open_invoices:
                partner_allowed_invoice_numbers = self.partner_id.allowed_invoice_numbers
                all_partner_open_invoices = self.env['account.invoice'].search_count(
                    [('partner_id', '=', self.partner_id.id), ('state', '=', 'open')])
                if all_partner_open_invoices >= partner_allowed_invoice_numbers:
                    raise ValidationError(_('Customer %s exceed allowed number of invoices %s.' % (
                        self.partner_id.name, self.partner_id.allowed_invoice_numbers)))
        return super(SaleOrder, self).action_confirm()
