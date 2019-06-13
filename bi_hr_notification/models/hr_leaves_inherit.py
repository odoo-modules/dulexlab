# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, time
from datetime import datetime


class HrLeaveTypeInherit(models.Model):
    _inherit = 'hr.leave.type'

    employee_notification = fields.Integer('Employee Notification')


class HrLeavesInherit(models.Model):
    _inherit = 'hr.leave'

    @api.multi
    def action_approve(self):
        for record in self:
            res = super(HrLeavesInherit, self).action_approve()
            beging_of_current_year = datetime.now().date().replace(month=1, day=1)
            end_of_current_year = datetime.now().date().replace(month=12, day=31)
            leave_objs = self.search([('employee_id', '=', record.employee_id.id),
                                      ('request_date_from', '>=', beging_of_current_year),
                                      ('request_date_to', '<=', end_of_current_year),
                                      ('holiday_status_id', '=', record.holiday_status_id.id),
                                      ('state', '=', 'validate'),
                                      ])
            if record.holiday_status_id.request_unit == 'day':
                total_leaves = sum([rec.number_of_days_display for rec in leave_objs])
            else:
                total_leaves = sum([rec.number_of_hours_display for rec in leave_objs])

            if record.holiday_status_id.employee_notification and total_leaves >= record.holiday_status_id.employee_notification:
                res_ids = []
                for user in self.env['res.users'].search([('partner_id', '!=', False)]):
                    if user.has_group('hr.group_hr_manager'):
                        res_ids.append(user.partner_id.id)

                if record.employee_id.parent_id.address_home_id:
                    res_ids.append(record.employee_id.parent_id.address_home_id.id)

                if total_leaves:
                    vals = {'subject': 'Employee Leave Notification',
                            'body_html': 'Dears' + ',<br/>' +
                                         'Notification for <strong>' + record.employee_id.name + "</strong>,<br/>"
                                         + record.holiday_status_id.name + "<strong> (" + str(total_leaves)
                                         + ") </strong><br/>",
                            'recipient_ids': [(6, 0, res_ids)],
                            'author_id': self.env.ref('base.partner_admin').id,
                            }
                    mail = self.env['mail.mail'].create(vals)
                    mail.send()
            return res
