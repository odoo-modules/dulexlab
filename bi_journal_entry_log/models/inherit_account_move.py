# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, fields, api, _


class JournalEntry(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'mail.thread']

    state = fields.Selection([('draft', 'Unposted'), ('posted', 'Posted')], string='Status',
                             required=True, readonly=True, copy=False, default='draft',
                             help='All manually created new journal entries are usually in the status \'Unposted\', '
                                  'but you can set the option to skip that status on the related journal. '
                                  'In that case, they will behave as journal entries automatically created by the '
                                  'system on document validation (invoices, bank statements...) and will be created '
                                  'in \'Posted\' status.', track_visibility='onchange')
    name = fields.Char(string='Number', required=True, copy=False, default='/', track_visibility='onchange')
    ref = fields.Char(string='Reference', copy=False, track_visibility='onchange')
    date = fields.Date(required=True, states={'posted': [('readonly', True)]}, index=True,
                       default=fields.Date.context_today, track_visibility='onchange')

    @api.model
    def create(self, vals):
        move = super(JournalEntry, self).create(vals)
        move.log_message()
        return move

    @api.multi
    def log_message(self):
        def _format_message(message_description, tracked_values):
            message = ''
            if message_description:
                message = '<span>%s</span>' % message_description
            for name, values in tracked_values.items():
                message += '<div> &nbsp; &nbsp; &bull; <b>%s</b>: ' % name
                message += '%s</div>' % values
            return message

        for line in self:
            if line:
                msg_values = {
                    'Created by': self.create_uid.name,
                    'Created on': self.create_date.strftime('%Y-%m-%dT%H:%M:%S'),
                    'Last Updated on': self.write_date.strftime('%Y-%m-%dT%H:%M:%S'),
                    'Last Updated by': self.write_uid.name}
                msg = _format_message(_('New Journal Entry Created.'), msg_values)
                line.message_post(body=msg)

    # @api.multi
    # def button_cancel(self):
    #     update = super(JournalEntry, self).button_cancel()
    #     return update.message_post(body="Status: Posted -->Unposted")

    # @api.multi
    # def last_update(self):
    #     for state in self:
    #         print(state)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    account_id = fields.Many2one('account.account', string='Account', required=True, index=True,
                                 ondelete="cascade", domain=[('deprecated', '=', False)],
                                 default=lambda self: self._context.get('account_id', False),
                                 track_visibility='onchange')
    partner_id = fields.Many2one('res.partner', string='Partner', ondelete='restrict', track_visibility='onchange')
    name = fields.Char(string="Label", track_visibility='onchange')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', index=True,
                                          track_visibility='onchange')
    amount_currency = fields.Monetary(string="Amount in Currency", track_visibility='onchange')
    debit = fields.Monetary(default=0.0, currency_field='company_currency_id', track_visibility='onchange')
    credit = fields.Monetary(default=0.0, currency_field='company_currency_id', track_visibility='onchange')
    tax_ids = fields.Many2many('account.tax', string='Taxes',
                               domain=['|', ('active', '=', False), ('active', '=', True)], track_visibility='onchange')
