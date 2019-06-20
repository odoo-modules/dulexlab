# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    responsible_user = fields.Many2one('res.users', string="Responsible User", related="journal_id.responsible_user")
