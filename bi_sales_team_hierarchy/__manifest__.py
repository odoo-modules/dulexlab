# -*- coding: utf-8 -*-
{
    'name': "BI Sales Team Hierarchy",
    'summary': "BI Sales Team Hierarchy",
    'description': """ 
            This module creates new fields and customize Sales module.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Sale',
    'version': '0.1',
    'depends': ['sale_stock', 'sale', 'stock', 'account', 'base'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/inherit_res_users.xml',
        'views/inherit_sale_order.xml',
        'views/inherit_crm_team.xml',
        'views/inherit_account_invoice.xml',
        'views/inherit_stock_picking.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
