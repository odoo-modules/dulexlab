# -*- coding: utf-8 -*-
from odoo import models, fields, api


class InheritedStockPicking(models.Model):
    _inherit = 'stock.picking'

    sales_person = fields.Many2one('res.users', string="Sales Person", related='sale_id.user_id')
    sales_team = fields.Many2one('crm.team', string="Sales Team", related='sale_id.team_id')
    area = fields.Many2one('new.area', string="Area", related='sale_id.area')
    team_supervisor = fields.Many2one('res.users', srting="Term Supervisor", related='sale_id.team_supervisor')
    team_leader = fields.Many2one('res.users', srting="Term Leader")
    driver_name = fields.Many2one('res.partner', string="Driver Name")
    car_number = fields.Many2one('fleet.vehicle', string="Car Number")
    is_from_sale = fields.Boolean(string='From Sale Order', compute='is_from_so')

    @api.model
    def create(self, vals):
        res = super(InheritedStockPicking, self).create(vals)
        if 'sale_id' in vals:
            res.write({'car_number': res.sale_id.car_number.id, 'driver_name': res.sale_id.driver_name.id})
        print(res.name)
        return res

    @api.multi
    def is_from_so(self):
        for pick in self:
            if pick.sale_id:
                pick.is_from_sale = True
                pick.write({'is_from_sale': 'True',
                            'car_number': pick.sale_id.car_number.id, 'driver_name': pick.sale_id.driver_name.id})

    @api.onchange('car_number')
    @api.multi
    def set_driver_name(self):
        for pick in self:
            if pick.car_number and pick.car_number.driver_id and pick.car_number.driver_id.id:
                pick.driver_name = pick.car_number.driver_id.id
