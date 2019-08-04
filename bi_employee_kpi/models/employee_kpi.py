# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class EmployeeKPI(models.Model):
    _name = 'employee.kpi'
    _description = 'Employee KPI'


    name = fields.Char(string='Name', required=1)
    salary_rule_id = fields.Many2one('hr.salary.rule', string='Salary Rule', required=1)



class EmployeeKPILine(models.Model):
    _name = 'employee.kpi.line'
    _description = 'Employee KPI Line'
    _rec_name = 'employee_kpi_id'


    employee_kpi_id = fields.Many2one('employee.kpi', string='KPI', required=1, ondelete='cascade')
    payslip_id = fields.Many2one('hr.payslip', string='Payslip')
    apply = fields.Boolean(string='Apply?')