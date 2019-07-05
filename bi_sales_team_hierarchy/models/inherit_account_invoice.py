# -*- coding: utf-8 -*-
from odoo import models, fields, api


class InheritedAccountInvoice(models.Model):
    _inherit = 'account.invoice'

    area = fields.Many2one('new.area', string="Area", )
    team_supervisor = fields.Many2one('res.users', srting="Team Supervisor")
    team_leader = fields.Many2one('res.users', srting="Team Leader")
    driver_name = fields.Many2one('res.partner', string="Driver Name")
    car_number = fields.Many2one('fleet.vehicle', string="Car Number")
    user_id = fields.Many2one('res.users', string='Salesperson', track_visibility='onchange',
        readonly=True, states={'draft': [('readonly', False)]}, default=False)
    team_id = fields.Many2one('crm.team', string='Sales Team', default=False, oldname='section_id')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', readonly=True)
