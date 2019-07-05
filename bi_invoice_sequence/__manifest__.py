# -*- coding: utf-8 -*-
{
    'name': "BI Invoice Sequence",
    'summary': "BI Invoice Sequence",
    'description': """ 
            This module changes invoice sequence depends on invoice is taxable or not!".
     """,
    'author': "BI Solutions Development Team",
    'category': 'Accounting',
    'version': '0.1',
    'depends': ['account_accountant', 'base'],
    'data': [
        'data/sequence_data.xml',
        'views/inherit_account_inv.xml',
        'reports/custom_invoice_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
