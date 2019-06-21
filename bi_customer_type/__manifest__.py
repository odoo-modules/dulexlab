# -*- coding: utf-8 -*-
{
    'name': "BI Sales Customer Type",
    'summary': "BI Sales Customer Type",
    'description': """ 
            This module creates new model(customer type) and adds new field to customer and adds customer type to SO && Invoice.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Sale',
    'version': '0.1',
    'depends': ['sale', 'sale_management', 'base', 'account'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/customer_type_view.xml',
        'views/inherit_res_partner_view.xml',
        'views/inherit_sale_order_view.xml',
        'views/inherit_account_invoice_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
