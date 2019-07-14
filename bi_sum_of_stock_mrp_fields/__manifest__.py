# -*- coding: utf-8 -*-
{
    'name': "BI Sum Of Stock/Mrp Fields",
    'summary': "BI Sum Of Picking and Bom Fields",
    'description': """ 
            This module adds sum attribute to stock.picking and mrp.bom models.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Stock',
    'version': '0.1',
    'depends': ['stock', 'base', 'mrp'],
    'data': [
        'views/inherit_stock_picking_view.xml',
        'views/inherit_mrp_bom_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
