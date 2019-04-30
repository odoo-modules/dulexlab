# -*- coding: utf-8 -*-
{
    'name': "BI Total Volume",
    'summary': "BI Total Volume",
    'description': """ 
            This module customizes Sales Order and Stock, adding 2 new fields (sum of products volume on SO,
            total volume for initial demand and total volume for done).
     """,
    'author': "BI Solutions Development Team",
    'category': 'Sale',
    'version': '0.1',
    'depends': ['sale', 'sale_stock', 'stock', 'base'],
    'data': [
        'views/inherit_sale_order.xml',
        'views/inherit_stock_picking.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
