# -*- coding: utf-8 -*-
{
    'name': "Bi Accounting Customizations",

    'summary': """Bi Accounting Customizations""",

    'description': """
        1- Create Picking after validating the refund invoice.\n
        2- Add new group to hide return button from delivery,receipt.\n

    """,

    'author': "Bi Development Team",
    'website': "http://bisolutions.com/",
    'category': 'Account',
    'version': '12.0.0.1.0',
    'depends': ['account', 'account_accountant', 'stock'],

    # always loaded
    'data': [
        # 'reports/invoices.xml',
        'security/security.xml',
        'wizard/invoice_validate_wizard.xml',
        'views/account_invoice_inherit.xml',
        'views/stock_picking_inherit.xml',
    ],
}
