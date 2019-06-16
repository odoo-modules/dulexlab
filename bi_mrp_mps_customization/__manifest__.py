# -*- coding: utf-8 -*-
{
    'name': "Bi MRP MPS Report Customizations",
    'summary': """MPS Report Customization""",
    'description': """
        1- Prevent writing in (To Receive / To Supply / Produce) section in MPS report.\n
        2- Make top down partitioning for quantity.\n
    """,
    'author': "Bi Development Team",
    'website': "http://bisolutions.com/",
    'category': 'Account',
    'version': '12.0.0.1.0',
    'depends': ['mrp_mps'],
    'data': [
        "views/editing_mrp_mps_template.xml",
    ],

}
