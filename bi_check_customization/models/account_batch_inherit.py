from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BiAccountBatchPaymentInherit(models.Model):
    _inherit = "account.batch.payment"

    state = fields.Selection(
        [('draft', 'New'), ('sent', 'Sent'), ('under_collection', 'Under Collection'), ('collection', 'Collection'),
         ('reconciled', 'Reconciled')], readonly=True, default='draft', copy=False)

    @api.multi
    def action_account_entries(self):
        return {
            'domain': "[('payment_batch_id', '=', %s)]" % self.id,
            'name': _("Entries"),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window'
        }
