# -*- coding: utf-8 -*-
{
    'name': "BI Icon Team",
    'summary': "BI Icon Team",
    'description': """ 
            This module adds icon team to SO, invoice, and so invoices analysis, also adds team leader and team supervisor to invoices analysis.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Sale',
    'version': '0.1',
    'depends': ['base', 'sale', 'account'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/icon_team_view.xml',
        'views/inherit_sale_order_view.xml',
        'views/inherit_account_invoice_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
