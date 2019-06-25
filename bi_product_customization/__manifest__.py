# -*- coding: utf-8 -*-
{
    'name': "BI Product Customization",
    'summary': "BI Product Customization",
    'description': """ 
        Adding Fields:\n
            1 - Color: Char \n
            2 - Packaging Desc.: Char\n
            3 - Effective Date: Date.\n
            3 - Validity Period (Months): Integer.\n
     """,
    'author': "BI Solutions Development Team",
    'category': 'Product',
    'version': '0.1',
    'depends': ['product', 'stock'],
    'data': [
        'views/product_product.xml'
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
