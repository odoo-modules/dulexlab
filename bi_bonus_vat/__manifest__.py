# -*- coding: utf-8 -*-
{
    'name': "BI Bonus VAT",
    'summary': """BI Bonus VAT""",
    'description': """
        This Modules calculate the VAT for bonus products in SOs.
    """,
    'author': "Bi Development Team",
    'website': "http://bisolutions.com/",
    'category': 'Sale',
    'version': '12.0',
    'depends': ['sale', 'universal_discount_customization'],
    'data': [
        'views/product.xml',
        'views/sale_order.xml',
        'views/account_invoice_inherit_view.xml',
    ],
    'sequence': 1,
}
