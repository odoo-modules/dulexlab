# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountInvoiceInherit(models.Model):
    _inherit = 'account.invoice'
