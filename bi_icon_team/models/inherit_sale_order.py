# -*- coding: utf-8 -*-
from odoo import models, fields, api


class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'

    icon_team = fields.Many2one('icon.team', string="Icon Team")

    @api.multi
    def _prepare_invoice(self):
        res = super(InheritSaleOrder, self)._prepare_invoice()
        res['icon_team'] = self.icon_team.id if self.icon_team else False
        return res
