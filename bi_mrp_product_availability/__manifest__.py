# -*- coding: utf-8 -*-
{
    'name': "BI MRP Product Availability",
    'summary': "BI MRP Product Availability",
    'description': """ 
            This module adds constrain on product in manufacturing  order if bill of material qty less than available qty in row material location.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Manufacturing',
    'version': '0.1',
    'depends': ['mrp'],
    'data': [
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
