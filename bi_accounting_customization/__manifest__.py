# -*- coding: utf-8 -*-
{
    'name': "Bi Accounting Customizations",

    'summary': """Bi Accounting Customizations""",

    'description': """
        1- Hide the default discount column from the invoice layout and adding a new discounts column based on the price list.\n
        2- \n

    """,

    'author': "Bi Development Team",
    'website': "http://bisolutions.com/",
    'category': 'Account',
    'version': '12.0.0.1.0',
    'depends': ['account', 'account_accountant', 'stock'],

    # always loaded
    'data': [
        # 'reports/invoices.xml',
        'wizard/invoice_validate_wizard.xml',
        'views/account_invoice_inherit.xml',
    ],
}
