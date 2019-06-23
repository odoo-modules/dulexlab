# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'

    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', required=True)
    team_id = fields.Many2one('crm.team', related='user_id.sale_team_id')
    area = fields.Many2one('new.area', string="Area", related='user_id.area', readonly=False)
    team_supervisor = fields.Many2one('res.users', related='team_id.team_supervisor', srting="Team Supervisor")
    team_leader = fields.Many2one('res.users', related='team_id.user_id', srting="Team Leader")
    # vehicle_id = fields.Many2one('fleet.vehicle')
    driver_name = fields.Many2one('res.partner', related='car_number.driver_id', readonly=False, string="Driver Name",
                                  required=True)
    car_number = fields.Many2one('fleet.vehicle', string="Car Number")

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(InheritSaleOrder, self)._prepare_invoice()
        invoice_vals['area'] = self.area.id or False
        invoice_vals['team_supervisor'] = self.team_supervisor.id or False
        invoice_vals['team_leader'] = self.team_leader.id or False
        invoice_vals['driver_name'] = self.driver_name.id or False
        invoice_vals['car_number'] = self.car_number.id or False
        return invoice_vals


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    _description = "Sales Advance Payment Invoice"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        invoice = super(SaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        if invoice:
            invoice.write({
                'area': order.area.id or False,
                'team_supervisor': order.team_supervisor.id or False,
                'team_leader': order.team_leader.id or False,
                'driver_name': order.driver_name.id or False,
                'car_number': order.car_number.id or False,
            })
        return invoice
