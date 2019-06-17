# -*- coding: utf-8 -*-

from odoo import fields, models, _, api
from odoo.exceptions import UserError, ValidationError
import datetime


class QuotationCancelReason(models.TransientModel):
    _name = "quotation.cancel.reason"

    reason_id = fields.Many2one('cancel.reason', string="Cancel Reason", required=True)

    @api.one
    def submit_reason(self):
        if self.reason_id:
            quotation = self.env['sale.order'].search([('id', '=', self._context.get('sale_order_id'))])
            quotation.write({
                'reason_id': self.reason_id.id,
            })
            quotation.action_cancel()
        else:
            raise ValidationError(_("Please select a reason for cancellation"))
