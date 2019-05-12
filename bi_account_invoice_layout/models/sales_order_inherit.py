# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    # @api.multi
    # def _prepare_invoice(self):
    #     res = super(SaleOrderInherit, self)._prepare_invoice()


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    public_price_lst = fields.Monetary(string='Public Price', compute='get_public_price_lst', store=True)
    phd_disc = fields.Float(string='PHD %', store=True, compute='get_discounts_pricelist')
    dd_disc = fields.Float(string='DD %', store=True, compute='get_discounts_pricelist')
    cd_disc = fields.Float(string='CD %', store=True, compute='get_discounts_pricelist')

    @api.depends('order_id.pricelist_id')
    def get_discounts_pricelist(self):
        for val in self:
            val.phd_disc = val.order_id.pricelist_id.phd_disc
            val.dd_disc = val.order_id.pricelist_id.dd_disc
            val.cd_disc = val.order_id.pricelist_id.cd_disc

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLineInherit, self)._prepare_invoice_line(qty)
        res['phd_disc'] = self.phd_disc
        res['dd_disc'] = self.dd_disc
        res['cd_disc'] = self.cd_disc
        return res

    @api.multi
    @api.depends('price_unit')
    def get_public_price_lst(self):
        for line in self:
            prod_public_price_rate = self.env['ir.config_parameter'].sudo().get_param('prod_public_price_rate')
            line.public_price_lst = line.price_unit * float(prod_public_price_rate)
