# -*- coding: utf-8 -*-
{
    'name': "BI Assets Modification",
    'summary': "BI customize assets and add total sum field to some columns",
    'description': """ 
            This module adds new attribute to gross value, residual value, and accumulated depreciation columns.
     """,
    'author': "BI Solutions Development Team",
    'category': 'Accounting',
    'version': '0.1',
    'depends': ['account_accountant', 'bi_assets_je_customization', 'base'],
    'data': [
        'views/inherit_account_asset_asset_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
