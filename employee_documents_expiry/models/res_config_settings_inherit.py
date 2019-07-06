# -*-	coding:	utf-8	-*-
from odoo import api, fields, models
import ast


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    documents_expiration_groups_ids = fields.Many2many('res.groups', 'doc_exp_group_rel', 'ex_set_id', 'ex_gp_id',
                                                'HR Documents Expiration Mail Groups', )

    def set_values(self):
        set_param = self.env['ir.config_parameter'].set_param
        set_param('documents_expiration_groups_ids', (self.documents_expiration_groups_ids.ids))
        super(ResConfigSettings, self).set_values()

    @api.multi
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        documents_expiration_groups_ids = self.env['ir.config_parameter'].sudo().get_param('documents_expiration_groups_ids')
        if documents_expiration_groups_ids:
            res.update(
                documents_expiration_groups_ids=ast.literal_eval(documents_expiration_groups_ids),
            )
        return res
