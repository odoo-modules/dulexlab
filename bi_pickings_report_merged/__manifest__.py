{
    'license': 'LGPL-3',
    "name": "BI DulexLab Pickings Merge -PDF",
    "version": "1",
    'sequence': 1,
    "author": "BI Solutions Development Team",
    "category": "DulexLab Pickings",
    "summary": "Export excel (or Print) report based on the driver with all Delivery order details (with accumulated the products QTY).",
    "depends": ["sale_management", "stock", "bi_sales_team_hierarchy"],
    "data": [
        'security/ir.model.access.csv',
        'views/stock_picking_merge_action.xml',
        'report/stock_picking_report.xml',
    ],
    "installable": True
}
