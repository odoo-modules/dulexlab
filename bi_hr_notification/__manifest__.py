# -*- coding: utf-8 -*-
{
    'name': "BI HR Notification",
    'summary': "BI HR Notification",
    'description': """ 
            This module add some notification related to hr module.
     """,
    'author': "BI Solutions Development Team",
    'category': 'hr',
    'version': '0.1',
    'depends': ['base', 'hr', 'hr_payroll'],
    'data': [
        'views/hr_employee_inherit_view.xml',
        'views/hr_leave_type_inherit_view.xml',
        'views/notification_cron.xml',
        'views/bi_conf_settings_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
