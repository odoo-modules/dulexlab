from odoo import models, fields, api, _


class ManufacturingWorkOrder(models.Model):
    _inherit = 'mrp.workorder'

    @api.multi
    def print_mo_record(self):
        report = self.env.ref('bi_batch_manufacturing_record_report.report_batch_manufacturing_record')
        return report.report_action(docids=self, config=False)
