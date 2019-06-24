from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BiAccountBatchPaymentInherit(models.Model):
    _inherit = "account.batch.payment"

    state = fields.Selection(
        [('draft', 'New'), ('sent', 'Sent'), ('under_collection', 'Under Collection'), ('collection', 'Collection'),
         ('reconciled', 'Reconciled')], readonly=True, default='draft', copy=False)

    partners_ids = fields.Many2many('res.partner', relation='partners_account_batch_rel', column1='batch_id',
                                    column2='partner_id', string="Partners", compute='get_lines_data')

    memos_lines = fields.Text('Memo', compute='get_lines_data', store=True)
    journal_id = fields.Many2one('account.journal', string='Journal', domain=[('type', '=', 'bank')],
                                 required=True, readonly=True,
                                 states={
                                     'draft': [('readonly', False)],
                                 })
    bank_id = fields.Many2one('account.journal', string='Bank', domain=[('type', '=', 'bank')],
                              required=True, readonly=True,
                              states={
                                  'draft': [('readonly', False)],
                                  'sent': [('readonly', False)],
                                  'under_collection': [('readonly', False)]
                              })
    partner_name = fields.Many2one('res.partner', string="Partner")

    @api.depends('payment_ids')
    def get_lines_data(self):
        for record in self:
            record.partners_ids = record.payment_ids.mapped('partner_id.id')
            if record.payment_ids:
                record.write({'partner_name': record.payment_ids[0].partner_id.id})

            memos = []
            s = ', '
            for line in record.payment_ids:
                if line.communication:
                    memos.append(line.communication)
            record.memos_lines = s.join(memos)

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
