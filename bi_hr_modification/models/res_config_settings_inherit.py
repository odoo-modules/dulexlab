# -*-	coding:	utf-8	-*-
from odoo import api, fields, models
import ast


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    overtime_groups_ids = fields.Many2many('res.groups', 'overtime_group_setting_rel', 'setting_id',
                                                      'group_id', 'Contract Expiration Mail Groups', )

    def set_values(self):
        set_param = self.env['ir.config_parameter'].set_param
        set_param('overtime_groups_ids', (self.overtime_groups_ids.ids))
        super(ResConfigSettings, self).set_values()

    @api.multi
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        overtime_groups_ids = self.env['ir.config_parameter'].sudo().get_param('overtime_groups_ids')

        if overtime_groups_ids:
            res.update(
                overtime_groups_ids=ast.literal_eval(overtime_groups_ids),
            )

        return res
