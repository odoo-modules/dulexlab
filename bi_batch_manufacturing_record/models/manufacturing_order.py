# -*- coding: utf-8 -*-
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class ManufacturingOrder(models.Model):
    _inherit = 'mrp.production'

    batch_number = fields.Char(string="Batch Number", compute="_get_batch_number", store=True)

    @api.one
    @api.depends('product_id', 'date_planned_start')
    def _get_batch_number(self):
        if self.product_id and self.state != 'cancel':
            previous_mos = self.search([
                ('date_planned_start', '<', (self.date_planned_start + relativedelta(months=1)).strftime('%Y-%m-01 00:00:00')),
                ('date_planned_start', '>=', self.date_planned_start.strftime('%Y-%m-01 00:00:00')),
                ('state', '!=', 'cancel'),
                ('product_id', '=', self.product_id.id)
            ])
            self.batch_number = str(self.product_id.batch_sequence) + '/' + str("{0:0=3d}".format(len(previous_mos)))

    @api.multi
    def action_cancel(self):
        res = super(ManufacturingOrder, self).action_cancel()
        for order in self:
            order.batch_number = order.batch_number + ' - Cancelled'
        return res
