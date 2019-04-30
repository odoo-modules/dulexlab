# -*- coding: utf-8 -*-
{
    'name': "Bi Multi Invoice Payment",

    'summary': """Bi Multi Invoice Payment""",

    'description': """
        This Module will add same functionality like odoo v8 Payment screen where based on partner selection it will load invoices and make full or partial payment.
    """,

    'author': "Bi Development Team",
    'website': "http://bisolutions.com/",
    'category': 'Account',
    'version': '12.0.0.1.0',
    'depends': ['base','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_payment_inherit.xml',
    ],
}
