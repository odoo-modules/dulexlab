# -*- coding: utf-8 -*-
{
    'name': "BI Dulex Purchase Modification",
    'summary': "BI Dulex Purchase Modification",
    'description': """ 
            This module adds received Qty and remaining Qty to purchase order line,
            new column called tags,
            print tag in PO report
     """,
    'author': "BI Solutions Development Team",
    'category': 'Purchase',
    'version': '0.1',
    'depends': ['purchase', 'base'],
    'data': [
        'views/inherit_purchase_order_lines_view.xml',
        'views/inherit_purchase_order_view.xml',
        'reports/purchase_order_report_inherit.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
