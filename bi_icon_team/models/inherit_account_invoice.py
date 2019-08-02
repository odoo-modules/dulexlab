# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    icon_team = fields.Many2one('icon.team', string="Icon Team")

    @api.model
    def _prepare_refund(self, invoice, date_invoice=None, date=None, description=None, journal_id=None):
        res = super(AccountInvoice, self)._prepare_refund(invoice, date_invoice, date, description, journal_id)
        res['icon_team'] = self.icon_team.id if self.icon_team else False
        return res


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    def _get_icon_team(self):
        if self.partner_id and self.partner_id.icon_team:
            return self.partner_id.icon_team.id
        else:
            return False

    def _get_team_leader(self):
        if self.invoice_id and self.invoice_id.team_leader:
            return self.invoice_id.team_leader.id
        else:
            return False

    def _get_team_supervisor(self):
        if self.invoice_id and self.invoice_id.team_supervisor:
            return self.invoice_id.team_supervisor.id
        else:
            return False

    @api.multi
    @api.depends('partner_id.icon_team')
    def _set_customer_type(self):
        for record in self:
            if record.partner_id and record.partner_id.icon_team:
                record.icon_team = record.partner_id.icon_team.id
            else:
                record.icon_team = False

    @api.multi
    @api.depends('invoice_id.team_supervisor', 'invoice_id.team_leader')
    def _set_team_data(self):
        for record in self:
            if record.invoice_id and record.invoice_id.team_supervisor:
                record.team_supervisor = record.invoice_id.team_supervisor.id
            else:
                record.team_supervisor = False
            if record.invoice_id and record.invoice_id.team_leader:
                record.team_leader = record.invoice_id.team_leader.id
            else:
                record.team_leader = False

    icon_team = fields.Many2one('icon.team', string="Icon Team", default=_get_icon_team)
    team_leader = fields.Many2one('res.users', string="Team Leader", default=_get_team_leader)
    team_supervisor = fields.Many2one('res.users', string="Team Supervisor", default=_get_team_supervisor)

    def _select(self):
        return super(AccountInvoiceReport, self)._select() +\
               ", sub.icon_team as icon_team, sub.team_leader as team_leader, sub.team_supervisor as team_supervisor"

    def _sub_select(self):
        return super(AccountInvoiceReport, self)._sub_select() +\
               ", ai.icon_team as icon_team, ai.team_leader as team_leader, ai.team_supervisor as team_supervisor"

    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by() +\
               ", ai.icon_team, ai.team_leader, ai.team_supervisor"
