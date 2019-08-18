# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.tools.float_utils import float_is_zero


class CrossoveredBudgetLine(models.Model):
    _inherit = "crossovered.budget.lines"

    planned_practical_variance = fields.Monetary(compute='_compute_variance_amount', string='Variance Amount',
                                                 store=True)
    # planned_practical_variance_percent = fields.Monetary(compute='_compute_variance_amount', string='Variance Percent',
    #                                                      store=True)

    @api.multi
    @api.depends('planned_amount', 'practical_amount')
    def _compute_variance_amount(self):
        for line in self:
            line.planned_practical_variance = line.planned_amount - line.practical_amount
            # if not float_is_zero(line.planned_amount, 2):
            #     line.planned_practical_variance_percent = line.planned_practical_variance / line.planned_amount
            #     print(line.planned_practical_variance_percent)
            # else:
            #     line.planned_practical_variance_percent = 0.0
