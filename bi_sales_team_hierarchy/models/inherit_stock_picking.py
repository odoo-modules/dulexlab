# -*- coding: utf-8 -*-
from odoo import models, fields, api

class InheritedStockPicking(models.Model):
    _inherit = 'stock.picking'

    area = fields.Many2one('new.area', string="Area", related='sale_id.area')
    team_supervisor = fields.Many2one('res.users', srting="Term Supervisor", related='sale_id.team_supervisor')
    team_leader = fields.Many2one('res.users', srting="Term Leader", related='sale_id.team_leader')
    driver_name = fields.Many2one('driver.name', string="Driver Name", related='sale_id.driver_name')
    car_number = fields.Many2one('car.number', string="Car Number", related='sale_id.car_number')