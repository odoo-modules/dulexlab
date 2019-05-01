# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'

    invoice_payment_ids = fields.One2many('account.payment.invoice', 'payment_id', string='Invoices Payments')
    total_payment_invoice = fields.Monetary('Total Payment Of Invoices', compute='_compute_payment_invoice', store=True)
    writeoff2_account_id = fields.Many2one('account.account', string="Difference Account(2)",
                                           domain=[('deprecated', '=', False)], copy=False)
    writeoff_amount = fields.Monetary(string='Writeoff Amount')
    writeoff2_amount = fields.Monetary(string='Writeoff Amount(2)')

    @api.multi
    @api.depends('invoice_payment_ids', 'invoice_payment_ids.allocation_amount')
    def _compute_payment_invoice(self):
        for rec in self:
            rec.total_payment_invoice = sum([l.allocation_amount for l in rec.invoice_payment_ids]) or 0.0

    # getting open invoices related to this partner
    @api.onchange('payment_type', 'partner_id', 'partner_type')
    def _onchange_payment_information(self):
        if self.invoice_payment_ids:
            self.invoice_payment_ids = [(5)]
        account_invoice_obj = self.env['account.invoice']
        account_invoice_payment_vals = []
        if self.partner_id:
            if self.payment_type == 'inbound' and self.partner_type == 'customer':
                invoice_ids = account_invoice_obj.search(
                    [('partner_id', '=', self.partner_id.id), ('type', '=', 'out_invoice'), ('state', '=', 'open')])
            if self.payment_type == 'outbound' and self.partner_type == 'supplier':
                invoice_ids = account_invoice_obj.search(
                    [('partner_id', '=', self.partner_id.id), ('type', '=', 'in_invoice'), ('state', '=', 'open')])

            for invoice in invoice_ids:
                account_invoice_payment_vals.append((0, 0,
                                                     {'invoice_id': invoice.id, 'account_id': invoice.account_id.id,
                                                      'date_due': invoice.date_due,
                                                      'amount_total': invoice.amount_total,
                                                      'residual': invoice.residual,
                                                      'currency_id': invoice.currency_id.id, }))
            self.invoice_payment_ids = account_invoice_payment_vals

    def _create_payment_entry(self, amount):
        """ Create a journal entry corresponding to a payment, if the payment references invoice(s) they are reconciled.
            Return the journal entry.
        """
        if self.total_payment_invoice:
            move = self.env['account.move'].create(self._get_move_vals())
            invoice_ids = []
            # generating journal items for each invoice
            for invoice_payment in self.invoice_payment_ids:
                if invoice_payment.allocation_amount:
                    invoice_ids.append(invoice_payment.invoice_id.id)
                    invoice_payment_amount = invoice_payment.allocation_amount * (
                                self.payment_type in ('outbound', 'transfer') and 1 or -1)
                    aml_obj = self.env['account.move.line'].with_context(check_move_validity=False)
                    debit, credit, amount_currency, currency_id = aml_obj.with_context(
                        date=self.payment_date)._compute_amount_fields(invoice_payment_amount, self.currency_id,
                                                                       self.company_id.currency_id)

                    # Write line corresponding to invoice payment
                    counterpart_aml_dict = self._get_shared_move_line_vals(debit, credit, amount_currency, move.id,
                                                                           False)
                    counterpart_aml_dict.update(self._get_counterpart_move_line_vals(invoice_payment.invoice_id))
                    counterpart_aml_dict.update({'currency_id': currency_id})
                    counterpart_aml = aml_obj.create(counterpart_aml_dict)
                    # reconcile the invoice receivable/payable line(s) with the payment
                    invoice_payment.invoice_id.register_payment(counterpart_aml)

            # Write counterpart lines
            debit, credit, amount_currency, currency_id = aml_obj.with_context(
                date=self.payment_date)._compute_amount_fields(amount, self.currency_id, self.company_id.currency_id)
            if not self.currency_id.is_zero(self.amount):
                if not self.currency_id != self.company_id.currency_id:
                    amount_currency = 0
                liquidity_aml_dict = self._get_shared_move_line_vals(credit, debit, -amount_currency, move.id,
                                                                     False)
                liquidity_aml_dict.update(self._get_liquidity_move_line_vals(-amount))
                aml_obj.create(liquidity_aml_dict)

            # Assign invoices to payment
            if invoice_ids:
                self.invoice_ids = [(6, 0, invoice_ids)]

            # Reconcile with the invoices
            if self.payment_difference:
                debit, credit, amount_currency, currency_id = aml_obj.with_context(
                    date=self.payment_date)._compute_amount_fields(self.payment_difference, self.currency_id,
                                                                   self.company_id.currency_id)
                if self.payment_difference_handling == 'reconcile':
                    # writeoff journal items
                    if self.writeoff_account_id and self.writeoff_amount:
                        writeoff_line = self._get_shared_move_line_vals(0, 0, 0, move.id, False)
                        debit_wo, credit_wo, amount_currency_wo, currency_id = aml_obj.with_context(
                            date=self.payment_date)._compute_amount_fields(self.writeoff_amount, self.currency_id,
                                                                           self.company_id.currency_id)
                        writeoff_line['name'] = self.writeoff_label
                        writeoff_line['account_id'] = self.writeoff_account_id.id
                        writeoff_line['debit'] = debit_wo
                        writeoff_line['credit'] = credit_wo
                        writeoff_line['amount_currency'] = amount_currency_wo
                        writeoff_line['currency_id'] = currency_id
                        aml_obj.create(writeoff_line)
                    # writeoff2 journal items
                    if self.writeoff2_account_id and self.writeoff2_amount:
                        writeoff_line = self._get_shared_move_line_vals(0, 0, 0, move.id, False)
                        debit_wo, credit_wo, amount_currency_wo, currency_id = aml_obj.with_context(
                            date=self.payment_date)._compute_amount_fields(self.writeoff2_amount, self.currency_id,
                                                                           self.company_id.currency_id)
                        writeoff_line['name'] = self.writeoff_label
                        writeoff_line['account_id'] = self.writeoff2_account_id.id
                        writeoff_line['debit'] = debit_wo
                        writeoff_line['credit'] = credit_wo
                        writeoff_line['amount_currency'] = amount_currency_wo
                        writeoff_line['currency_id'] = currency_id
                        aml_obj.create(writeoff_line)
                else:
                    # Write line corresponding to invoice payment
                    counterpart_aml_dict = self._get_shared_move_line_vals(debit, credit, amount_currency, move.id,
                                                                           False)
                    counterpart_aml_dict.update(self._get_counterpart_move_line_vals(self.invoice_ids))
                    counterpart_aml_dict.update({'currency_id': currency_id})
                    aml_obj.create(counterpart_aml_dict)
            # validate the payment
            if not self.journal_id.post_at_bank_rec:
                move.post()

            return move
        else:
            return super(AccountPaymentInherit, self)._create_payment_entry(amount)

    # inherit for calculating payment difference with invoices payments
    @api.depends('invoice_ids', 'amount', 'payment_date', 'currency_id', 'total_payment_invoice', 'invoice_payment_ids')
    def _compute_payment_difference(self):
        for pay in self:
            if pay.invoice_ids and not pay.total_payment_invoice:
                payment_amount = -pay.amount if pay.payment_type == 'outbound' else pay.amount
                pay.payment_difference = pay._compute_payment_amount() - payment_amount
            elif pay.total_payment_invoice:
                payment_amount = -pay.amount if pay.payment_type == 'outbound' else pay.amount
                total_payment_invoice = -pay.total_payment_invoice if pay.payment_type == 'outbound' else pay.total_payment_invoice
                pay.payment_difference = total_payment_invoice - payment_amount

    # constrain on payment difference amount with writeoff amounts
    @api.constrains('payment_difference', 'writeoff_amount', 'writeoff2_amount')
    def payment_difference_constrain(self):
        for rec in self:
            if rec.payment_difference and rec.payment_difference_handling == 'reconcile':
                total_writeoff_amount = rec.writeoff_amount + rec.writeoff2_amount
                if rec.payment_difference != total_writeoff_amount:
                    raise UserError(_('Total Difference Amount Must Be Equal To Payment Difference Amount!'))
