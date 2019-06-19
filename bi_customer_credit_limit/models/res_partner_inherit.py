# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    use_credit_limit = fields.Boolean(string='Credit Limit')
    credit_limit_amount = fields.Boolean('Credit Limit On Amount')
    credit_limit_open_invoices = fields.Boolean('Credit Limit On Open Invoices')
    allowed_amount = fields.Float(string='Allowed Amount')
    allowed_invoice_numbers = fields.Integer(string='Allowed Invoices Number')

    @api.multi
    @api.constrains('allowed_amount')
    def check_credit_limit_amount(self):
        for rec in self:
            if rec.credit_limit_amount and rec.allowed_amount <= 0.0:
                raise ValidationError(_('Allowed amount must be greater than zero.'))

    @api.multi
    @api.constrains('allowed_invoice_numbers')
    def check_credit_limit_invoice_numbers(self):
        for rec in self:
            if rec.credit_limit_open_invoices and rec.allowed_invoice_numbers <= 0:
                raise ValidationError(_('Allowed invoice number must be greater than zero.'))

    @api.onchange('credit_limit_amount')
    def clear_allowed_amount(self):
        for rec in self:
            if not rec.credit_limit_amount:
                rec.allowed_amount = 0

    @api.onchange('credit_limit_open_invoices')
    def clear_allowed_invoice_number(self):
        for rec in self:
            if not rec.credit_limit_open_invoices:
                rec.allowed_invoice_numbers = 0
