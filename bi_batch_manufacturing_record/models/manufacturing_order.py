# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class ManufacturingOrder(models.Model):
    _inherit = 'mrp.production'

    batch_number = fields.Char(string="Batch Number", compute="_get_batch_number", store=True)

    @api.one
    @api.depends('product_id', 'date_planned_start')
    def _get_batch_number(self):
        if self.product_id and self.state != 'cancel':
            previous_mos = self.search([
                ('date_planned_start', '<',
                 (self.date_planned_start + relativedelta(months=1)).strftime('%Y-%m-01 00:00:00')),
                ('date_planned_start', '>=', self.date_planned_start.strftime('%Y-%m-01 00:00:00')),
                ('state', '!=', 'cancel'),
                ('product_id', '=', self.product_id.id)
            ])
            print(self.date_planned_start.month)
            first_part = False
            if self.date_planned_start.month == self.product_id.batch_month:
                first_part = self.product_id.batch_sequence
            elif self.date_planned_start.month > self.product_id.batch_month:
                first_part = self.product_id.batch_sequence + \
                             (self.date_planned_start.month - self.product_id.batch_month) * self.product_id.batch_step
            elif self.date_planned_start.month < self.product_id.batch_month:
                first_part = self.batch_sequence + (12 - (
                        self.date_planned_start.month - self.product_id.batch_month)) * self.product_id.batch_step
            else:
                raise ValidationError(
                    _("Please Make sure your order has Deadline start and the product has batch number and batch step"))
            self.batch_number = str(first_part) + '/' + str("{0:0=3d}".format(len(previous_mos)))

    @api.multi
    def action_cancel(self):
        res = super(ManufacturingOrder, self).action_cancel()
        for order in self:
            order.batch_number = order.batch_number + ' - Cancelled'
        return res
