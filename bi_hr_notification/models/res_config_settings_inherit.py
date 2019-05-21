# -*-	coding:	utf-8	-*-
from odoo import api, fields, models
import ast


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    check_id_expiration = fields.Integer('Check Id Expiration Before', )
    check_contract_expiration = fields.Integer('Check contract Expiration Before', )

    def set_values(self):
        set_param = self.env['ir.config_parameter'].set_param
        set_param('check_id_expiration', (self.check_id_expiration))
        set_param('check_contract_expiration', (self.check_contract_expiration))
        super(ResConfigSettings, self).set_values()

    @api.multi
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param

        res.update(
            check_id_expiration=int(get_param('check_id_expiration')),
            check_contract_expiration=int(get_param('check_contract_expiration'))
        )
        return res
