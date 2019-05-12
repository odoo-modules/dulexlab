# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ProductSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    prod_public_price_rate = fields.Float('Product Price Rate', default=0.0)

    def set_values(self):
        set_param = self.env['ir.config_parameter'].set_param

        set_param('prod_public_price_rate', (self.prod_public_price_rate))

        super(ProductSettings, self).set_values()

    @api.multi
    def get_values(self):
        res = super(ProductSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            prod_public_price_rate=float(get_param('prod_public_price_rate')),
        )
        return res
