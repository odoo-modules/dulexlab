# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


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
        if check_id_expiration:
            employee_objs = self.env['hr.employee'].sudo().search([])
            for manager in employee_objs.mapped('parent_id'):
                body = ''
                current_date = fields.date.today()
                table_header = "<table class='table'><thead><tr><th scope='col'>Employee Name</th><th scope='col'>Job Position</th><th scope='col'>Expiration Date</th><th scope='col'>Diff. Days</th></tr></thead><tbody>"
                for employee in self.env['hr.employee'].sudo().search(
                        [('parent_id', '=', manager.id), ('id_expiry_date', '!=', False)]):
                    id_expiry_date = employee.id_expiry_date
                    diff_date = (id_expiry_date - current_date).days
                    if diff_date > 0 < check_id_expiration:
                        emp_link = str("<a href=#id=" + str(
                            employee.id) + "&view_type=form&model=hr.employee>" + employee.name + "</a>")
                        body += str(
                            "<tr><th scope='row'>" + emp_link + "</th><td>" + str(
                                employee.job_id.name or ' ') + "</td><td>" + str(
                                employee.id_expiry_date) + "</td><td style='color:red'>" + str(
                                diff_date) + "</td></tr>")

                etable = "</tbody></table>"
                vals = {'subject': 'Identification Expiry Date Mail **',
                        'body_html': 'Dear ' + str(manager.name) + ',<br/>' + str(table_header) + str(body) + str(
                            etable),
                        'email_to': manager.work_email,
                        'author_id': self.env.ref('base.partner_admin').id,
                        }

                mail = self.env['mail.mail'].create(vals)
                mail.send()

    @api.multi
    def contract_send_email(self):
        get_param = self.env['ir.config_parameter'].sudo().get_param
        check_contract_expiration = int(get_param('check_contract_expiration'))
        if check_contract_expiration:
            contract_objs = self.env['hr.contract'].sudo().search(
                [('state', '=', 'open'), ('date_end', '!=', False), ('employee_id.parent_id', '!=', False)])
            for contract in contract_objs:
                body = ''
                current_date = fields.date.today()
                table_header = "<table class='table'><thead><tr><th scope='col'>Employee Name</th><th scope='col'>Contract Date</th><th scope='col'>Expiration Date</th><th scope='col'>Diff. Days</th></tr></thead><tbody>"

                contract_expiry_date = contract.date_end
                diff_date = (contract_expiry_date - current_date).days
                if diff_date > 0 < check_contract_expiration:
                    emp_link = str("<a href=#id=" + str(
                        contract.id) + "&view_type=form&model=hr.employee>" + contract.employee_id.name + "</a>")
                    body += str(
                        "<tr><th scope='row'>" + emp_link + "</th><td>" + str(
                            contract.date_start or ' ') + "</td><td>" + str(
                            contract.date_end or ' ') + "</td><td style='color:red'>" + str(diff_date) + "</td></tr>")

                etable = "</tbody></table>"
                vals = {'subject': 'Contract Expiry Date Mail **',
                        'body_html': 'Dear ' + str(contract.employee_id.parent_id.name) + ',<br/>' + str(
                            table_header) + str(body) + str(etable),
                        'email_to': contract.employee_id.parent_id.id,
                        'author_id': self.env.ref('base.partner_admin').id,
                        }

                mail = self.env['mail.mail'].create(vals)
                mail.send()
