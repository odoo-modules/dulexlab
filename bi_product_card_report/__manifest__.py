{
    'name': "BI Product Card Report",
    'summary': "BI Product Card Report",
    'description': """ 
            This module generates xlsx reports to product card.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['stock', 'sale', 'purchase', 'report_xlsx'],
    'data': ['views/wizard_view.xml'],
    'installable': True,
    'auto_install': False,
    'sequence': 1,
}
