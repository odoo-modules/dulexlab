# -*- coding: utf-8 -*-
{
    'name': "BI MO Pause Reason",
    'summary': "BI MO Pause Reason",
    'description': """
            This module edit on mrp pause reason.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Manufacturing',
    'version': '0.1',
    'depends': ['mrp'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/pause_reason_wizard_view.xml',
        'views/mrp_workorder_pause_reason_view.xml',
        'views/mrp_workorder_inherit_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
