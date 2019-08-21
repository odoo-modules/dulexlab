# -*- coding: utf-8 -*-
{
    'name': "BI Cost SalePrice Margin Access",
    'summary': "BI hide cost, saleprice and margin fields from view",
    'description': """  
            This module adds 3 new groups to sales:
            - margin access
            - cost access
            - sales price access
     """,
    'author': "BI Solutions Development Team",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['sale_management', 'stock', 'sale_margin', 'base'],
    'data': [
        'security/groups.xml',
        'views/inherit_saleorder_view.xml',
        'views/inherit_productproduct_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
