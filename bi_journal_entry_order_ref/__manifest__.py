# -*- coding: utf-8 -*-
{
    'name': "Bi Journal Entry Order Reference",
    'summary': "Bi Account Customization",
    'description': """
    """,
    'author': "BI Solutions Development Team",
    'category': 'Accounting',
    'version': '0.1',
    'depends': ['base', 'stock_account'],
    'data': [
        'views/account_move_view.xml',
        'set_lines_ref.xml'
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 44
}
