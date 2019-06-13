# -*- coding: utf-8 -*-
{
    'name': "BI SalesOrder State Customization",
    'summary': "BI SalesOrder State Customization",
    'description': """ 
            This module adds new stage to state field related to pending button.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['sale', 'base'],
    'data': [
        'views/inherit_sale_order.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
