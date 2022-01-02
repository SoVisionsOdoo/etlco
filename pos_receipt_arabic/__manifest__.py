{
    'name': 'POS Arabic Receipt / POS Customized Receipt(Arabic Receipt)',
    'version': '15.0.5',
    'currency': 'EUR',
    'license': 'OPL-1',
    'description': """
POS Customized Receipt(Arabic Receipt)
        """,
    'depends': ['point_of_sale','l10n_sa_pos'],
    'qweb': [
        'static/src/xml/templates.xml',
    ],
    'data': ['views/pos_receipt_template.xml',
    ],
    'images': ['static/description/main_screenshot.jpg'],
    'auto_install': False,
}

