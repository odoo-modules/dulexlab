# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    parent_mo_id = fields.Many2one('mrp.production', string="Parent MO")

    def _log_manufacture_exception(self, documents, cancel=False):
        if documents:
            for item in next(iter(documents)):
                for object in item:
                    if object._name == 'mrp.production':
                        for move_line in self.move_raw_ids:
                            if move_line.product_id.id == object.product_id.id:
                                res = self.env['change.production.qty'].create({'mo_id': object.id, 'product_qty': move_line.product_uom_qty})
                                res.change_prod_qty()
                                break
                        if self.state == 'cancel':
                            object.action_cancel()

        return super(MrpProduction, self)._log_manufacture_exception(documents, cancel)
