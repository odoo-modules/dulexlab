# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, fields, api, _
import re
import uuid
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

from openerp.exceptions import ValidationError


class AccountInvoiceInhh(models.Model):
    _inherit = 'account.invoice'

    seq_un_taxed = fields.Char('Un-Taxed Sequence')

    @api.multi
    def action_invoice_open(self):
        res = super(AccountInvoiceInhh, self).action_invoice_open()
        for invoice in self:
            if invoice.state == 'open' and not invoice.tax_line_ids:
                invoice.seq_un_taxed = self.env['ir.sequence'].next_by_code('untaxed.invoice.seq')
        return res
