# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    customer_type = fields.Many2one('customer.type', string="Customer Type", related='partner_id.customer_type', store=True)


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    customer_type = fields.Many2one('customer.type', string="Customer Type", related='partner_id.customer_type', store=True)

    def _select(self):
        return super(AccountInvoiceReport, self)._select() + ", sub.customer_type as customer_type"

    def _sub_select(self):
        return super(AccountInvoiceReport, self)._sub_select() + ", ai.customer_type as customer_type"

    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by() + ", ai.customer_type"
