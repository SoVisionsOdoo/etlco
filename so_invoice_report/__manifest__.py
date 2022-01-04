# -*- coding: utf-8 -*-
{
    'name': "Customer reprint invoice",
    'description': """
        1-Customer Invoice Reprint
        2-vendor invoice Reprint
    """,
    'author': "So Visions",
    'category': 'Sales',
    'version': '12.0.1.0.2',
    'depends': ['base', 'account','so_qr_invoice'],
    'data': [
        # 'views/customer_invoice_report_ar.xml',
        'views/impressiv_report_design.xml',
        'views/template.xml',
        'views/res_company.xml',
    ],
}
