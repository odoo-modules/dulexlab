# -*- coding: utf-8 -*-
{
    'name': "BI Quality Check Customization",
    'summary': "BI quality check customization",
    'description': """ 
            This module adds related fields from picking to quality check.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Stock',
    'version': '0.1',
    'depends': ['stock', 'base', 'purchase', 'quality_control'],
    'data': [
        'views/quality_check_inherited_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
