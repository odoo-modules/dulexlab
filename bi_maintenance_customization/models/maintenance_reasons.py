# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TechnicalReason(models.Model):
    _name = 'technical.reason'

    name = fields.Char(string='Reason', required=True)


class FailureReason(models.Model):
    _name = 'failure.reason'

    name = fields.Char(string='Reason', required=True)
