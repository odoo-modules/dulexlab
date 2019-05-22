# -*- coding: utf-8 -*-
{
    'name': "BI Journal Entry Log",
    'summary': "BI create log note to journal entry view",
    'description': """ 
            This module creates log note to journal entry form".
     """,
    'author': "BI Solutions Development Team",
    'category': 'Accounting',
    'version': '0.1',
    'depends': ['account_accountant', 'base'],
    'data': [
        'views/inherit_account_move.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
