# -*- coding: utf-8 -*-
from odoo import models, fields, api


class NewArea(models.Model):
    _name = 'new.area'

    name = fields.Char("Area", required=True)
