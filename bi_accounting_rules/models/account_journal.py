# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    responsible_user = fields.Many2one('res.users', string="Responsible User")
    to_view = fields.Boolean(string='To View Row', compute='to_view_value', store=False)
    to_view_s = fields.Boolean(string='To View')

    @api.multi
    def to_view_value(self):
        for record in self:
            print("XX")
            if self.user_has_groups('bi_accounting_rules.account_treasury_group_manager') \
               or self.env.user.id == 2                              \
               or record.responsible_user.id == self.env.user.id:
                record.to_view = True
                record.to_view_s = True
            else:
                record.to_view = False
                record.to_view_s = False
            print(record.to_view_s)
