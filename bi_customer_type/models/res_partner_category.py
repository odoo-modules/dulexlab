# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartnerCategory(models.Model):
    _name = 'partner.category'

    name = fields.Char(string="Partner Category")

