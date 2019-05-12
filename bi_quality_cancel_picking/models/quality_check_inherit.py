# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class QualityCheckInherit(models.Model):
    _inherit = 'quality.check'

    @api.multi
    def do_fail(self):
        """cancel failed stock moves"""
        if self.picking_id and self.product_id and self.product_id.categ_id.quality_control:
            move_id = self.picking_id.move_lines.filtered(
                lambda move: move.product_id == self.product_id)
            move_id._action_cancel()
        return super(QualityCheckInherit,self).do_fail()