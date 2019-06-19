# -*- coding: utf-8 -*-
{
    'name': "BI Accounting Rules",
    'summary': "BI Accounting Rules",
    'description': """ 
        This module adds record rules to both Account Journal and Account Payment Models.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Accounting',
    'version': '1.0',
    'depends': ['account'],
    'data': [
        'security/account_security.xml',
        'views/account_journal_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
