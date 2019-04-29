from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountBatchPaymentInherit(models.Model):
    _inherit = "account.move"

    payment_batch_id = fields.Many2one('account.batch.payment')
