# -*-	coding:	utf-8	-*-
from odoo import api, fields, models
import ast


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    check_id_expiration = fields.Integer('Check Id Expiration Before', )
    check_contract_expiration = fields.Integer('Check contract Expiration Before', )

    id_expiration_groups_ids = fields.Many2many('res.groups', 'ex_group_setting_rel', 'setting_id', 'group_id',
                                                'ID Expiration Mail Groups', )

    contract_expiration_groups_ids = fields.Many2many(
        comodel_name='res.groups', string='Contract Expiration Mail Groups',
        relation='contract_expiration_grps_rel',
        column1='sett_id',
        column2='grp_id')

    absence_days_groups_ids = fields.Many2many('res.groups', 'absence_group_setting_rel', 'setting_id',
                                               'group_id', 'Absence Mail Groups')
    id_reminder_after = fields.Integer('', default=30)
    contract_reminder_after = fields.Integer('', default=30)

    linked_days = fields.Integer('Linked Days')
    unlinked_days = fields.Integer('Un-Linked Days')

    def set_values(self):
        set_param = self.env['ir.config_parameter'].set_param
        set_param('check_id_expiration', (self.check_id_expiration))
        set_param('check_contract_expiration', (self.check_contract_expiration))
        set_param('id_expiration_groups_ids', (self.id_expiration_groups_ids.ids))
        set_param('absence_days_groups_ids', (self.absence_days_groups_ids.ids))
        set_param('contract_expiration_groups_ids', (self.contract_expiration_groups_ids.ids))
        set_param('id_reminder_after', (self.id_reminder_after))
        set_param('contract_reminder_after', (self.contract_reminder_after))
        set_param('linked_days', (self.linked_days))
        set_param('unlinked_days', (self.unlinked_days))
        super(ResConfigSettings, self).set_values()

    @api.multi
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        id_expiration_groups_ids = self.env['ir.config_parameter'].sudo().get_param('id_expiration_groups_ids')
        contract_expiration_groups_ids = self.env['ir.config_parameter'].sudo().get_param(
            'contract_expiration_groups_ids')
        absence_days_groups_ids = self.env['ir.config_parameter'].sudo().get_param(
            'absence_days_groups_ids')
        if id_expiration_groups_ids:
            res.update(
                id_expiration_groups_ids=ast.literal_eval(id_expiration_groups_ids),
            )
        if contract_expiration_groups_ids:
            res.update(
                contract_expiration_groups_ids=ast.literal_eval(contract_expiration_groups_ids),
            )
        if absence_days_groups_ids:
            res.update(
                absence_days_groups_ids=ast.literal_eval(absence_days_groups_ids),
            )

        res.update(
            check_id_expiration=int(get_param('check_id_expiration')),
            contract_reminder_after=int(get_param('contract_reminder_after')),
            id_reminder_after=int(get_param('id_reminder_after')),
            check_contract_expiration=int(get_param('check_contract_expiration')),
            unlinked_days=int(get_param('unlinked_days')),
            linked_days=int(get_param('linked_days')),

        )
        return res
