# -*- coding: utf-8 -*-
{
    'name': "BI HR Modification",
    'summary': "BI HR Modification",
    'description': """ 
            This module add some Customization related to hr module.
     """,
    'author': "BI Solutions Development Team",
    'category': 'hr',
    'version': '0.1',
    'depends': ['base', 'hr', 'hr_payroll', 'hr_attendance'],
    'data': [
        'views/hr_employee_inherit_view.xml',
        'views/hr_employee_overtime.xml',
        'views/payslip_inherit.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
