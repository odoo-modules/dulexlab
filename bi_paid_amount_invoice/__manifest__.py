# -*- coding: utf-8 -*-
{
    'name': "BI Invoice Paid Amount",
    'summary': "BI Invoice Paid Amount",
    'description': """ 
            This module adds a computed field computing the paid amount from the invoice, and add it to invoice tree view.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Accounting',
    'version': '0.1',
    'depends': ['account'],
    'data': [
        'views/account_invoice_tree.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
