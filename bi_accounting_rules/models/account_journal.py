# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    responsible_user = fields.Many2one('res.users', string="Responsible User")