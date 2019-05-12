# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountInvoiceLineInherit(models.Model):
    _inherit = 'account.invoice.line'

    public_price_lst = fields.Monetary(string='Public Price', compute='get_public_price_lst', store=True)
    phd_disc = fields.Float(string='PHD %')
    dd_disc = fields.Float(string='DD %')
    cd_disc = fields.Float(string='CD %')

    @api.multi
    @api.depends('price_unit')
    def get_public_price_lst(self):
        for line in self:
            prod_public_price_rate = self.env['ir.config_parameter'].sudo().get_param('prod_public_price_rate')
            line.public_price_lst = line.price_unit * float(prod_public_price_rate)


class AccountInvoiceInherit(models.Model):
    _inherit = 'account.invoice'

    discount_amount = fields.Monetary('', compute='get_discount_amount', store=True, track_visibility='onchange')

    @api.multi
    @api.depends('invoice_line_ids', 'invoice_line_ids.quantity', 'invoice_line_ids.price_unit',
                 'invoice_line_ids.discount')
    def get_discount_amount(self):
        for invoice in self:
            disc_amount = 0.0
            for line in invoice.invoice_line_ids:
                disc_amount += (line.quantity * line.price_unit * line.discount / 100)
            invoice.discount_amount = disc_amount
