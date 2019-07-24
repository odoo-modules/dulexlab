# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    batch_sequence = fields.Integer(string="Batch Sequence")
    batch_step = fields.Integer(string="Batch Step")
    batch_month = fields.Integer(string="Batch Change Date", default=-1)

    @api.multi
    def update_batch_sequence(self):
        for template in self.search([]):
            if fields.Date.today().month != template.batch_month:
                template.write({'batch_sequence': template.batch_sequence + template.batch_step})
                template.write({'batch_month': fields.Date.today().month})
