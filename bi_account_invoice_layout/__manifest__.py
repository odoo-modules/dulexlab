# -*- coding: utf-8 -*-
{
    'name': "Account invoice layout",

    'summary': """Account invoice layout""",

    'description': """
        1- Add 3 discount fields to SO and INV .\n
        2- Add 3 discount fields to invoice layout.\n

    """,

    'author': "Bi Development Team",
    'website': "http://bisolutions.com/",
    'category': 'Account',
    'version': '12.0.0.1.0',
    'depends': ['account', 'account_accountant', 'sale_management'],

    # always loaded
    'data': [
        'reports/invoices.xml',
        'views/account_invoice_inherit.xml',
    ],
}
