# -*- coding: utf-8 -*-
{
    'name': "Bi Check Customizations",

    'summary': """Bi Check Customizations""",

    'description': """""",

    'author': "Bi Development Team",
    'website': "http://bisolutions.com/",
    'category': 'Account',
    'version': '12.0.0.1.0',
    'depends': ['account_batch_payment'],

    # always loaded
    'data': [
        'security/security.xml',
        'wizard/batch_under_collection_wizard.xml',
        'views/account_payment_inherit.xml',
        'views/account_batch_inherit_view.xml',
    ],
}
