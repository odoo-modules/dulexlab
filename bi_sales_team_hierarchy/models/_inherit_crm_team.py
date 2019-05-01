# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SrmTeam(models.Model):
    _inherit = 'crm.team'

    team_supervisor = fields.Many2one('res.users', string= "Team Supervisor")