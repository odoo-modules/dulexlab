# -*- coding: utf-8 -*-
{
    'name': "BI Change Line Color",
    'summary': "BI change line color",
    'description': """ 
            This module changes the color of line when initial value != reserved value.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Stock',
    'version': '0.1',
    'depends': ['stock', 'base'],
    'data': [
        'views/inherited_stock_picking_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
