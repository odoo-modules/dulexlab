# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class WorkorderPauseWizard(models.TransientModel):
    _name = 'work.order.pause.wizard'

    reason_id = fields.Many2one(
        'work.order.pause.reason', string='Reason', required=True)

    @api.multi
    def confirm_pause(self):
        act_close = {'type': 'ir.actions.act_window_close'}
        active_ids = self._context.get('active_ids')
        if active_ids is None:
            return act_close
        assert len(active_ids) == 1, "Only 1 workorder ID expected"
        active_workorder = self.env['mrp.workorder'].browse(active_ids)
        active_workorder.pause_reason_id = self.reason_id.id
        active_workorder.with_context(order_paused=True).end_previous()
        return act_close
