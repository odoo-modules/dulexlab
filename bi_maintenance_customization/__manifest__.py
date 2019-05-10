# -*- coding: utf-8 -*-
{
    'name': "BI Maintenance Customization",
    'summary': "BI Maintenance Customization",
    'description': """
            This module add new fields in maintenance request.
     """,
    'author': "BI Solutions Development Team",
    'version': '0.1',
    'depends': ['maintenance', 'stock'],
    'data': [
        'security/maintenance_security_view.xml',
        'security/ir.model.access.csv',
        'views/res_config_setting_inherit_view.xml',
        'views/maintenance_request_line_view.xml',
        'views/maintenance_request_inherit_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
