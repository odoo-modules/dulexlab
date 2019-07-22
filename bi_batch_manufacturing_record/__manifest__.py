{
    "name": "BI Batch Manufacturing Record",
    'summary': "BI Batch Manufacturing Record",
    "version": "1",
    'sequence': 1,
    "author": "BI Solutions Development Team",
    'license': 'LGPL-3',
    "category": "Manufacturing",
    "summary": "Batch Manufacturing Record ",
    "depends": ["mrp", "bi_product_customization", "bi_mrp_order_customization"],
    "data": [
        "views/product_sequence_cron.xml",
        "views/product_product.xml",
        "views/manufacturing_order.xml",
    ],
    "installable": True
}


