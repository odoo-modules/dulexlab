# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
import ast
from dateutil.relativedelta import relativedelta


class IrCrone(models.Model):
    _inherit = 'ir.cron'

    @api.multi
    def employee_send_email(self):
        self.employee_expiration_mail()
        self.contract_send_email()

    @api.multi
    def employee_expiration_mail(self):
        get_param = self.env['ir.config_parameter'].sudo().get_param
        check_id_expiration = int(get_param('check_id_expiration'))
        id_reminder_after = int(get_param('id_reminder_after'))
        id_expiration_groups_ids = ast.literal_eval(
            (self.env['ir.config_parameter'].sudo().get_param('id_expiration_groups_ids')))
        partner_ids = []

        for group in self.env['res.groups'].search([('id', 'in', id_expiration_groups_ids)]):
            for user in group.users:
                if user.partner_id.id not in partner_ids:
                    partner_ids.append(user.partner_id.id)

        if check_id_expiration and partner_ids:
            table_header = "<table style='width: 100%; max-width: 100%; margin-bottom: 1rem; background-color: transparent;'><thead><tr><th scope='col'>Employee Name</th><th scope='col'>Job Position</th><th scope='col'>Expiration Date</th><th scope='col'>Diffrence Days</th></tr></thead><tbody>"
            body = ''
            etable = "</tbody></table>"

            current_date = fields.date.today()
            for employee in self.env['hr.employee'].sudo().search([('id_expiry_date', '!=', False)]):
                id_expiry_date = employee.id_expiry_date
                diff_date = (id_expiry_date - current_date).days
                if employee.id_next_notification == current_date:
                    if diff_date > 0 < check_id_expiration:
                        emp_link = str("<a target='_blank' href=#id=" + str(
                            employee.id) + "&view_type=form&model=hr.employee>" + employee.name + "</a>")
                        body += str(
                            "<tr><th scope='row'>" + emp_link + "</th><td style='text-align:center'>" + str(
                                employee.job_id.name or ' ') + "</td><td style='text-align:center'>" + str(
                                employee.id_expiry_date) + "</td><td style='text-align:center;color:red'>" + str(
                                diff_date) + "</td></tr>")

                elif not employee.id_next_notification:
                    employee.id_next_notification = current_date + relativedelta(days=+id_reminder_after)
                    emp_link = str("<a target='_blank' href=#id=" + str(
                        employee.id) + "&view_type=form&model=hr.employee>" + employee.name + "</a>")
                    body += str(
                        "<tr><th scope='row'>" + emp_link + "</th><td style='text-align:center'>" + str(
                            employee.job_id.name or ' ') + "</td><td style='text-align:center'>" + str(
                            employee.id_expiry_date) + "</td><td style='text-align:center;color:red'>" + str(
                            diff_date) + "</td></tr>")
            if body:
                vals = {'subject': 'Identification Expiry Date Mail **',
                        'body_html': 'Dears' + ',<br/>' + str(table_header) + str(body) + str(etable),
                        'recipient_ids': [(6, 0, partner_ids)],
                        'author_id': self.env.ref('base.partner_admin').id,
                        }
                mail = self.env['mail.mail'].create(vals)
                mail.send()

    @api.multi
    def contract_send_email(self):
        get_param = self.env['ir.config_parameter'].sudo().get_param
        check_contract_expiration = int(get_param('check_contract_expiration'))
        id_reminder_after = int(get_param('contract_reminder_after'))
        contract_expiration_groups_ids = ast.literal_eval(
            (self.env['ir.config_parameter'].sudo().get_param('contract_expiration_groups_ids')))
        partner_ids = []
        contract_objs = self.env['hr.contract'].sudo().search([('state', '=', 'open'), ('date_end', '!=', False)])

        for group in self.env['res.groups'].search([('id', 'in', contract_expiration_groups_ids)]):
            for user in group.users:
                if user.partner_id.id not in partner_ids:
                    partner_ids.append(user.partner_id.id)

        if check_contract_expiration and partner_ids and contract_objs:

            table_header = "<table style='width: 100%; max-width: 100%; margin-bottom: 1rem; background-color: transparent;'><strong><thead ><tr><th >Employee Name</th><th scope='col'>Contract Date</th><th scope='col'>Expiration Date</th><th scope='col'>Diffrence Days</th></tr></thead></strong><tbody>"
            body = ''
            etable = "</tbody></table>"

            for contract in contract_objs:
                current_date = fields.date.today()
                contract_expiry_date = contract.date_end
                diff_date = (contract_expiry_date - current_date).days

                if not contract.contract_next_notification:
                    contract.contract_next_notification = current_date + relativedelta(days=+id_reminder_after)
                    if diff_date > 0 < check_contract_expiration:
                        emp_link = str("<a href=#id=" + str(
                            contract.id) + "&view_type=form&model=hr.contract>" + contract.employee_id.name + "</a>")
                        body += str(
                            "<tr><th scope='row'>" + emp_link + "</th><td style='text-align:center'>" + str(
                                contract.date_start or ' ') + "</td><td style='text-align:center'>" + str(
                                contract.date_end or ' ') + "</td><td style='text-align:center;color:red'>" + str(
                                diff_date) + "</td></tr>")
                elif contract.contract_next_notification == current_date:
                    if diff_date > 0 < check_contract_expiration:
                        emp_link = str("<a href=#id=" + str(
                            contract.id) + "&view_type=form&model=hr.employee>" + contract.employee_id.name + "</a>")
                        body += str(
                            "<tr><th scope='row'>" + emp_link + "</th><td style='text-align:center'>" + str(
                                contract.date_start or ' ') + "</td><td style='text-align:center'>" + str(
                                contract.date_end or ' ') + "</td><td style='text-align:center;color:red'>" + str(
                                diff_date) + "</td></tr>")
            if body:
                vals = {'subject': 'Contract Expiry Date Mail **',
                        'body_html': 'Dears,<br/>' + str(
                            table_header) + str(body) + str(etable),
                        'recipient_ids': [(6, 0, partner_ids)],
                        'author_id': self.env.ref('base.partner_admin').id,
                        }
                mail = self.env['mail.mail'].create(vals)
                mail.send()
