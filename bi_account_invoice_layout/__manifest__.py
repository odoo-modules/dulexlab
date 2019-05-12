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
    'depends': ['account', 'account_accountant', 'sale_management', 'product'],

    # always loaded
    'data': [
        'reports/invoices.xml',
        'views/account_invoice_inherit.xml',
        'views/product_inherit.xml',
        'views/res_config_views.xml',
        'views/price_list_inherit.xml',
        'views/sale_order_inherit.xml',
    ],
}
