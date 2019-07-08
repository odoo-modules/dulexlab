# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    customer_type = fields.Many2one('customer.type', string="Customer Type", related='partner_id.customer_type', store=True)


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    def _get_customer_type(self):
        if self.partner_id and self.partner_id.customer_type:
            return self.partner_id.customer_type.id
        else:
            return False

    @api.multi
    @api.depends('partner_id.customer_type')
    def _set_customer_type(self):
        for record in self:
            if record.partner_id and record.partner_id.customer_type:
                record.customer_type = record.partner_id.customer_type.id
            else:
                record.customer_type = False

    customer_type = fields.Many2one('customer.type', string="Customer Type", default=_get_customer_type)

    def _select(self):
        return super(AccountInvoiceReport, self)._select() + ", sub.customer_type as customer_type"

    def _sub_select(self):
        return super(AccountInvoiceReport, self)._sub_select() + ", ai.customer_type as customer_type"

    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by() + ", ai.customer_type"
