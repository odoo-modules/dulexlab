# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class WorkOrderPauseReason(models.Model):
    _name = 'work.order.pause.reason'
    _description = 'Work Order Pause Reason'

    name = fields.Char('Reason', required=True, translate=True)
