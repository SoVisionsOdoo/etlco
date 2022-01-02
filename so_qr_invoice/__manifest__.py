# -*- coding: utf-8 -*-
{
    'name': "QR E-Invoice",

    'summary': """
        Adding QR code into Invoice
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Sovisions",
    'website': "http://www.sovisions.com",

    # for the full list
    'category': 'account',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'views/account_move.xml',
        'security/ir.model.access.csv',
    ],
    'qweb':[
        # 'views/move_webpage.xml',
    ]
}