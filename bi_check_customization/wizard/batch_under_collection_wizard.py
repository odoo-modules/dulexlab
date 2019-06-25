from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class UnderCollectionWizard(models.TransientModel):
    _name = "under.collection.batch.payment"

    journal_id = fields.Many2one('account.journal', string='Journal')
    debit_account_id = fields.Many2one('account.account', string='Debit Account')
    credit_account_id = fields.Many2one('account.account', string='Credit Account')

    @api.multi
    def action_confirm_payment(self):
        for val in self:
            ids = self.env.context.get('active_ids', [])
            batch_objs = self.env[self.env.context.get('active_model')].browse(ids)
            debit_account_id = val.debit_account_id.id
            credit_account_id = val.credit_account_id.id

            for batch in batch_objs:
                if batch.journal_id.type == 'bank':
                    for line in batch.payment_ids:
                        amount = line.amount
                        line_ids = []
                        move_dict = {
                            'payment_batch_id': batch.id,
                            'ref': line.communication,
                            'journal_id': val.journal_id.id,
                            # 'date': date,
                        }
                        if not line.due_date:
                            raise ValidationError(
                                _('Please set (Due Date) to payment No. %s to create entries') % line.name)
                        if debit_account_id:
                            debit_line = (0, 0, {
                                'name': line.communication,
                                'partner_id': line.partner_id.id,
                                'account_id': debit_account_id,
                                'journal_id': val.journal_id.id,
                                'date_maturity': line.due_date,
                                'batch_id': batch.id,
                                'debit': amount > 0.0 and amount or 0.0,
                            })
                            line_ids.append(debit_line)

                        if credit_account_id:
                            credit_line = (0, 0, {
                                'name': line.communication,
                                'partner_id': line.partner_id.id,
                                'account_id': credit_account_id,
                                'journal_id': val.journal_id.id,
                                'date_maturity': line.due_date,
                                'credit': amount > 0.0 and amount or 0.0,
                            })
                            line_ids.append(credit_line)

                        move_dict['line_ids'] = line_ids
                        move = self.env['account.move'].create(move_dict)
                        move.post()
            if batch.state == 'under_collection':
                batch.write({'state': 'collection'})
            elif batch.batch_type == 'outbound':
                batch.write({'state': 'collection'})
            else:
                batch.write({'state': 'under_collection'})

    @api.onchange('journal_id')
    def set_accounts(self):
        self.ensure_one()
        if self.journal_id:
            self.debit_account_id = self.journal_id.default_debit_account_id.id or False
            self.credit_account_id = self.journal_id.default_credit_account_id.id or False
