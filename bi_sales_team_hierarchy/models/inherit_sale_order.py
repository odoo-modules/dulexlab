# -*- coding: utf-8 -*-
from odoo import models, fields, api


class InheritedSaleOrder(models.Model):
    _inherit = 'sale.order'

    area = fields.Many2one('new.area', string="Area", related='user_id.area', readonly=False)
    team_supervisor = fields.Many2one('res.users', related='team_id.team_supervisor', srting="Team Supervisor")
    team_leader = fields.Many2one('res.users', related='team_id.user_id', srting="Team Leader")
    driver_name = fields.Many2one('driver.name', string="Driver Name")
    car_number = fields.Many2one('car.number', string="Car Number")

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(InheritedSaleOrder, self)._prepare_invoice()
        invoice_vals['area'] = self.area.id or False
        invoice_vals['team_supervisor'] = self.team_supervisor.id or False
        invoice_vals['team_leader'] = self.team_leader.id or False
        invoice_vals['driver_name'] = self.driver_name.id or False
        invoice_vals['car_number'] = self.car_number.id or False
        return invoice_vals
