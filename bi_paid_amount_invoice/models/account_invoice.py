# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # fields.Float(string="Paid Amount", compute="get_paid_amount")
    paid_amount = fields.Monetary(string='Paid Amount', currency_field='currency_id',
                                  readonly=True, compute='get_paid_amount',
                                  help="Total amount paid in the currency of the invoice.")

    @api.multi
    def get_paid_amount(self):
        for record in self:
            record.paid_amount = record.amount_total_signed - record.residual_signed
