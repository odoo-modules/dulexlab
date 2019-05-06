# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CarNumber(models.Model):
    _name = 'car.number'

    name = fields.Char("Car No.", required=True)
