# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime
import time
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    id_expiry_date = fields.Date('Identification Expiry Date')
    id_next_notification = fields.Date(copy=False)
    emp_code = fields.Char('Code')

    linked_absence = fields.Integer('Linked Absence')
    unlinked_absence = fields.Integer('Un-linked Absence')

    @api.model
    def attendance_notification(self):
        for employee in self.search([]):
            table_header = "<table style='width: 100%;padding:10px;'><tbody><tr><td style='width:33%;padding:10px;border:1px solid gray'>Employee Name</td><td style='width:33%;padding:10px;border:1px solid gray'>Employee Code</td><td style='width:33%;padding:10px;border:1px solid gray'>Last Check Out From</td></tr>"
            table_data = ''
            table_end = '</tbody></table>'
            recipient_ids = []
            year_from = time.strftime('%Y-01-01')
            today = fields.Datetime.now()
            attendance_obj = self.env['hr.attendance'].search([('employee_id', '=', employee.id),
                                                               ('check_out', '>=', year_from),
                                                               ('check_out', '<', today)],
                                                              order='check_out desc', limit=1)
            last_check_out = attendance_obj.check_out

            leave_obj = self.env['hr.leave'].search(
                [('state', '=', 'validate'), ('employee_id', '=', employee.id), ('date_from', '>=', last_check_out),
                 ('holiday_status_id.request_unit', '=', 'day'), ], order='date_from desc', limit=1)

            if leave_obj.date_to:
                d_frm_obj = datetime.strptime(str(leave_obj.date_to), DEFAULT_SERVER_DATETIME_FORMAT)
                d_to_obj = datetime.strptime(str(today), DEFAULT_SERVER_DATETIME_FORMAT)
                diff = (d_to_obj - d_frm_obj).days

                if employee.unlinked_absence and (diff > employee.unlinked_absence):
                    table_data += "<tr><td style='width:33%;padding:10px;border:1px solid gray'>" + employee.name + "</td><td style='width:33%;padding:10px;border:1px solid gray'>" + str(
                        employee.emp_code or ' ') + "</td><td style='width:33%;padding:10px;border:1px solid gray'>" + str(
                        diff) + "/days</td></tr>"
                    recipient_ids.append(employee.parent_id.address_home_id.id)
                    if recipient_ids:
                        mail_data = {'subject': 'linked absence mail notification',
                                     'body_html': 'Dears' + ',<br/>' + table_header + table_data + table_end,
                                     'recipient_ids': [(6, 0, recipient_ids)],
                                     'author_id': self.env.ref('base.partner_admin').id,
                                     }
                        mail = self.env['mail.mail'].create(mail_data)
                        mail.send()
