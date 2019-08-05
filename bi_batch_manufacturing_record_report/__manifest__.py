{
    "name": "BI Batch Manufacturing Report -PDF",
    'summary': "BI Batch Manufacturing Report -PDF",
    "version": "1",
    'sequence': 1,
    "author": "BI Solutions Development Team",
    'license': 'LGPL-3',
    "category": "Manufacturing Report",
    "summary": "Batch Manufacturing Report for Manufacturing Order.",
    "depends": ["mrp", "bi_product_customization", "bi_mrp_order_customization",
                "bi_batch_manufacturing_record", 'mrp_workorder'],
    "data": [
        'report/batch_record_report.xml',
        'views/mrp_workorder_form_inherit.xml',
    ],
    "installable": True
}


