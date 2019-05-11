# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class PriceListInherit(models.Model):
    _inherit = 'product.pricelist'

    phd_disc = fields.Float(string='PHD %')
    dd_disc = fields.Float(string='DD %')
    cd_disc = fields.Float(string='CD %')
