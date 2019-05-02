# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    use_credit_limit = fields.Boolean(string='Credit Limit')
    credit_limit_type = fields.Selection([('amount', 'Amount'), ('open_invoices', 'Open Invoices')],
                                         string='Credit Limit Type')
    allowed_amount = fields.Float(string='Credit Limit Amount')
    allowed_invoice_numbers = fields.Integer(string='Invoices Number')

    @api.onchange('credit_limit_type')
    def clear_allowed_amount(self):
        for rec in self:
            if rec.credit_limit_type != 'amount':
                rec.allowed_amount = 0
            elif rec.credit_limit_type != 'open_invoices':
                rec.allowed_invoice_numbers = 0
