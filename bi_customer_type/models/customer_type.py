# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CustomerType(models.Model):
    _name = 'customer.type'

    name = fields.Char("Customer Type", required=True)
