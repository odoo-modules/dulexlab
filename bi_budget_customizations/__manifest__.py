# -*- coding: utf-8 -*-
{
    'name': "BI Budget Customizations",
    'summary': """BI Budget Customizations""",
    'description': """
        This Modules Add variance to budgets lines and budget analysis.
    """,
    'author': "BI Development Team",
    'website': "http://bisolutions.com/",
    'category': 'Sale',
    'version': '12.0',
    'depends': ['base', 'account_budget'],
    'data': [
        'views/account_budget_inherit.xml',
    ],
    'sequence': 1,
}
