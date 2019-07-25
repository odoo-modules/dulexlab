# -*- coding: utf-8 -*-
{
    'name': "BI BoM Cost Structure Update",
    'summary': """BI BoM Cost Structure Update""",
    'description': """
        1- Add Available Quantity on locations in bom cost structure.\n
    """,
    'author': "Bi Development Team",
    'website': "http://bisolutions.com/",
    'category': 'MRP',
    'version': '12.0.0.1.0',
    'depends': ['mrp', 'stock'],
    'data': [
        "views/bom_form.xml",
        "report/report_bom_structure.xml",
    ],
    'sequence': 1,
}
