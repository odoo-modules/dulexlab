# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from dateutil.relativedelta import relativedelta


class HRPayslip(models.Model):
    _inherit = "hr.payslip"

    absence_days = fields.Float('Absence Days')
    absence_amount = fields.Float('Leaves Amount Deduction')
    accumulate_leave_amount = fields.Float('Accumulate Leaves Amount')

    @api.multi
    def compute_sheet(self):
        for payslip in self:
            payslip.get_absence_days()
            payslip.get_accumulate_leaves()
        super(HRPayslip, self).compute_sheet()
        # return True

    @api.multi
    def get_absence_days(self):
        for rec in self:
            start_date = fields.Date.from_string(rec.date_from)
            end_date = fields.Date.from_string(rec.date_to)
            days = 0
            absence_days = 0
            day_lst = []

            leaves_obj = self.env['hr.leave'].search(
                [('employee_id', '=', rec.employee_id.id), ('date_from', '>=', rec.date_from),
                 ('date_to', '<=', rec.date_to), ('state', '=', 'validate')])
            leaves_days = sum([leave.number_of_days_display for leave in leaves_obj])

            for attendance in rec.employee_id.resource_calendar_id.attendance_ids:
                if dict(attendance._fields['dayofweek'].selection).get(attendance.dayofweek) not in day_lst:
                    day_lst.append(dict(attendance._fields['dayofweek'].selection).get(attendance.dayofweek))

            while start_date <= end_date:

                days += 1
                last_date = rec.date_from + relativedelta(days=+days)

                date = fields.Datetime.from_string(start_date).date()
                if date.strftime("%A") in day_lst:
                    attendance_obj = self.env['hr.attendance'].search(
                        [('employee_id', '=', rec.employee_id.id), ('check_in', '<', last_date),
                         ('check_in', '>=', start_date)])

                    if not attendance_obj:
                        absence_days += 1
                start_date = last_date

            rec.absence_days = abs(absence_days - leaves_days)
            rec.absence_amount = (rec.contract_id.wage / 30) * rec.absence_days

        return {'absence_days': absence_days, 'leaves_days': leaves_days}

    @api.multi
    def get_accumulate_leaves(self):
        for rec in self:
            accumulate_objs = self.env['accumulate.leaves'].search(
                [('employee_id', '=', rec.employee_id.id), ('accumulate_date', '>=', rec.date_from),
                 ('accumulate_date', '<=', rec.date_to), ('state', '=', 'approved')])
            accumulate_leave_amount = sum([rec.total_amount for rec in accumulate_objs])
            rec.accumulate_leave_amount = accumulate_leave_amount

    @api.multi
    def action_payslip_done(self):
        res = super(HRPayslip, self).action_payslip_done()
        for rec in self:
            accumulate_objs = self.env['accumulate.leaves'].search(
                [('employee_id', '=', rec.employee_id.id), ('accumulate_date', '>=', rec.date_from),
                 ('accumulate_date', '<=', rec.date_to), ('state', '=', 'approved')])
            for acc in accumulate_objs:
                acc.payslip_id = rec.id
                acc.action_paid()
        return res

    @api.multi
    def refund_sheet(self):
        res = super(HRPayslip, self).refund_sheet()
        for payslip in self:
            accumulate_objs = self.env['accumulate.leaves'].search([('payslip_id', '=', payslip.id)])
            for acc in accumulate_objs:
                acc.state = 'cancel'
        return res
