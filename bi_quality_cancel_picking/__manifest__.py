# -*- coding: utf-8 -*-
{
    'name': "Bi Cancel Pickings Of Failed Quality Checks",

    'summary': """Bi Cancel Pickings Of Failed Quality Checks""",

    'description': """
        This Module cancels the stock moves of failed quality checks based on product category.
    """,

    'author': "Bi Development Team",
    'website': "http://bisolutions.com/",
    'category': 'Account',
    'version': '12.0.0.1.0',
    'depends': ['base','product','quality_control'],

    # always loaded
    'data': [
        'views/product_category_inherit_view.xml',
        'views/stock_picking_inherit_view.xml',
    ],
}
