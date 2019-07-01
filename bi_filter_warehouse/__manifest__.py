# -*- coding: utf-8 -*-
{
    'name': "BI Warehouse Filter In SO",
    'summary': "BI Warehouse Filter In SO",
    'description': """ 
        This module adds 'Appear in SO' field in warehouses to be set as a domain in so warehouse.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Sale Stock',
    'version': '0.1',
    'depends': ['stock', 'sale'],
    'data': [
        'views/stock_warehouse_form.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
