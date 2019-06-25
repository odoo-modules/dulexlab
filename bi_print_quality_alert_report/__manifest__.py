# -*- coding: utf-8 -*-
{
    'name': "BI Print Quality Alert Report",
    'summary': "BI quality alert report",
    'description': """ 
            This module prints Quality alert as PDF report.
     """,
    'author': "BI Solutions Development Team",
    'category': 'accounting',
    'version': '0.1',
    'depends': ['base', 'quality_control'],
    'data': [
        'views/report_quality_alert_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
