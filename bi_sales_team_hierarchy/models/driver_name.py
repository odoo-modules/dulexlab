# -*- coding: utf-8 -*-
from odoo import models, fields, api


class NewDriversName(models.Model):
    _name = 'driver.name'

    name = fields.Char("Driver Name", required=True)
