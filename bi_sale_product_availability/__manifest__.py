# -*- coding: utf-8 -*-
{
    'name': "BI Sale Product Availability",
    'summary': "BI Sale Product Availability",
    'description': """ 
            This module adds constrain on product in sale order line if requested qty less than available qty in location.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Sale',
    'version': '0.1',
    'depends': ['sale_management', 'stock'],
    'data': [
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
