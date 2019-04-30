# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AccountPaymentInvoice(models.Model):
    _name = 'account.payment.invoice'

    payment_id = fields.Many2one('account.payment', string='Payment')
    invoice_id = fields.Many2one('account.invoice', string='Invoice')
    account_id = fields.Many2one('account.account', string='Account')
    date_invoice = fields.Date(string='Date')
    date_due = fields.Date(string='Due Date')
    amount_total = fields.Monetary(string='Original Amount')
    residual = fields.Monetary(string='Amount Due')
    currency_id = fields.Many2one('res.currency', string='Currency')
    allocation_amount = fields.Float(string='Allocation Amount')

    @api.constrains('allocation_amount', 'residual')
    def allocation_amount_constrain(self):
        for rec in self:
            if rec.allocation_amount < 0.0:
                raise UserError(_('Allocation Amount Must Be Greater Than 0.0!'))

            if rec.allocation_amount > rec.residual:
                raise UserError(_('Allocation Amount Greater Than Residual Amount!'))