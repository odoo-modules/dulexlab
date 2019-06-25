# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    area = fields.Many2one('new.area', string="Area")
    # team_member_ids = fields.One2many('crm.team', 'res_user_id', string='Channel Members')