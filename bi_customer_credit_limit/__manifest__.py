# -*- coding: utf-8 -*-
{
    'name': "BI Customer Credit Limit",
    'summary': "BI Customer Credit Limit",
    'description': """ 
            This module add customer credit limit.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Sale',
    'version': '0.1',
    'depends': ['sale_management'],
    'data': [
        'views/res_partner_inherit_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
