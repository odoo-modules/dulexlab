# -*- coding: utf-8 -*-
from odoo import models, fields, api


class IconTeam(models.Model):
    _name = 'icon.team'

    name = fields.Char(string="Name")
