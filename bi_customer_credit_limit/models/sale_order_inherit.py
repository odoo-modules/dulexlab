# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.constrains('partner_id')
    def check_customer_credit_limit(self):
        for order in self:
            if order.partner_id.use_credit_limit:
                if order.partner_id.credit_limit_type == 'amount':
                    partner_allowed_credit_limit_amount = order.partner_id.allowed_amount
                    partner_open_invoices = self.env['account.invoice'].search(
                        [('partner_id', '=', order.partner_id.id), ('state', '=', 'open')])
                    total_partner_due_amount = sum(invoice.residual for invoice in partner_open_invoices)
                    if partner_allowed_credit_limit_amount < (total_partner_due_amount + order.amount_total):
                        raise ValidationError(_('Customer %s exceed his credit limit amount %s %s.' % (
                            order.partner_id.name, order.partner_id.allowed_amount, order.currency_id.symbol)))

                elif order.partner_id.credit_limit_type == 'open_invoices':
                    partner_allowed_invoice_numbers = order.partner_id.allowed_invoice_numbers
                    all_partner_open_invoices = self.env['account.invoice'].search_count(
                        [('partner_id', '=', order.partner_id.id), ('state', '=', 'open')])
                    if all_partner_open_invoices > partner_allowed_invoice_numbers:
                        raise ValidationError(_('Customer %s exceed his credit invoices %s.' % (
                            order.partner_id.name, order.partner_id.allowed_invoice_numbers)))
