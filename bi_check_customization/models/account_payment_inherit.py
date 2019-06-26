from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountPaymentInherit(models.Model):
    _inherit = "account.payment"

    due_date = fields.Date('Due Date')

    @api.onchange('amount', 'currency_id')
    def _onchange_amount(self):
        jrnl_filters = self._compute_journal_domain_and_types()
        journal_types = jrnl_filters['journal_types']
        domain_on_types = [('type', 'in', list(journal_types))]
        return {'domain': {'journal_id': jrnl_filters['domain'] + domain_on_types}}
