# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    last_accumulate_date = fields.Date('Last Accumulate Date')
    name_ar = fields.Char('Arabic Name')
    emp_code = fields.Char('Code')
    hiring_date = fields.Date('Hiring Date')

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', '|', '|', '|', ('name', operator, name), ('emp_code', operator, name),
                      ('name_ar', operator, name), ('barcode', operator, name), ('work_email', operator, name)]
        employee = self.search(domain + args, limit=limit)
        return employee.name_get()
