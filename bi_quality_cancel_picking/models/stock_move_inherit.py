# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class StockMoveInherit(models.Model):
    _inherit = 'stock.move'

    quality_check_status = fields.Selection([('pass', 'Pass'), ('fail', 'Fail')], string='Quality Check Status',
                                            default='pass', copy=False)

    @api.constrains('quality_check_status', 'quantity_done')
    def _quality_check_constrain(self):
        for rec in self:
            if rec.quality_check_status == 'fail' and rec.quantity_done != 0.0:
                raise UserError(_('You Cannot add quantity done for failed quality checks products!'))