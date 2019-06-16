# -*- coding: utf-8 -*-
{
    'name': "BI SaleOrder Cancel Modification",
    'summary': "BI SaleOrder Cancel Button Customization",
    'description': """ 
            This module customize cancel button and adds the cancel reason to log note.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Sale',
    'version': '0.1',
    'depends': ['sale', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'views/inherit_sale_order.xml',
        'views/cancel_reason_view.xml',
        'wizard/quotation_cancel.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
