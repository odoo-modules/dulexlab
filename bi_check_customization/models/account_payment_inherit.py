from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountPaymentInherit(models.Model):
    _inherit = "account.payment"

    due_date = fields.Date('Due Date')
