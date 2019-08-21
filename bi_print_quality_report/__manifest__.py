# -*- coding: utf-8 -*-
{
    'name': "BI Print quality Reports",
    'summary': "BI quality reports",
    'description': """ 
            This module prints quality check items as PDF report.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Quality',
    'version': '0.1',
    'depends': ['base', 'quality_control'],
    'data': [
        'views/inherit_quality_check_view.xml',
        'reports/report_quality_check_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
