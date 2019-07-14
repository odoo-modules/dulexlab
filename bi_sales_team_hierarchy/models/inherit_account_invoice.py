# -*- coding: utf-8 -*-
from odoo import models, fields, api


class InheritedAccountInvoice(models.Model):
    _inherit = 'account.invoice'

    area = fields.Many2one('new.area', string="Area", )
    team_supervisor = fields.Many2one('res.users', srting="Team Supervisor")
    team_leader = fields.Many2one('res.users', srting="Team Leader")
    driver_name = fields.Many2one('res.partner', string="Driver Name")
    car_number = fields.Many2one('fleet.vehicle', string="Car Number")
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', readonly=True)

    @api.onchange('user_id')
    def get_user_team_values(self):
        for invoice in self:
            if invoice.user_id:
                invoice.team_id = invoice.user_id.sale_team_id.id
                invoice.area = invoice.user_id.area.id
                invoice.team_leader = invoice.user_id.sale_team_id.user_id.id
                invoice.team_supervisor = invoice.user_id.sale_team_id.team_supervisor.id
