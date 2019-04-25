# -*- coding: utf-8 -*-
{
    'name': "BI Sale Taxable",
    'summary': "BI Sale Taxable",
    'description': """ 
            This module add selection to make order is taxable.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Sale',
    'version': '0.1',
    'depends': ['sale_management'],
    'data': [
        'views/sale_order_inherit_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
