# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, fields, api, _
import re
import uuid
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

from openerp.exceptions import ValidationError
from num2words import num2words
from odoo.tools import float_compare


class AccountInvoiceInhh(models.Model):
    _inherit = 'account.invoice'

    invoice_sequence = fields.Char('Serial')

    @api.multi
    def action_invoice_open(self):
        res = super(AccountInvoiceInhh, self).action_invoice_open()
        for invoice in self:
            if invoice.state == 'open' and not invoice.tax_line_ids and not invoice.invoice_sequence:
                invoice.invoice_sequence = self.env['ir.sequence'].next_by_code('untaxed.invoice.seq')
            elif invoice.state == 'open' and invoice.tax_line_ids:
                invoice.invoice_sequence = self.env['ir.sequence'].next_by_code('taxed.invoice.seq')
            elif (invoice.state == 'paid' and float_compare(invoice.amount_total + invoice.amount_tax +
                                                            invoice.amount_untaxed, 0, precision_rounding=2) == 0):
                invoice.invoice_sequence = self.env['ir.sequence'].next_by_code('untaxed.invoice.seq')

        return res

    @api.multi
    def get_amount_total_words(self):
        for val in self:
            if val.amount_total:
                words = num2words(val.amount_total, lang='ar')

                if words.find(',') > 1:
                    unit, sub_unit = words.split(",")
                    words_currency = unit + val.currency_id.currency_unit_label + " , " + sub_unit + " " + \
                                     val.currency_id.currency_subunit_label + " فقط لا غير "
                    return words_currency

                else:
                    words = words + " " + val.currency_id.currency_unit_label + " فقط لا غير "
                    return words
