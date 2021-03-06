# -*- coding: utf-8 -*-
{
    'name': 'Studio customizations',
    'version': '14.0.1.0',
    'category': 'Studio',
    'description': u"""
This module has been generated by Odoo Studio.
It contains the apps created with Studio and the customizations of existing apps.
""",
    'author': 'Environmental Testing & Laboratories Co.',
    'depends': [
        'account',
        'base',
        'crm',
        'fleet',
        'hr',
        'hr_contract',
        'hr_expense',
        'hr_holidays',
        'hr_payroll',
        'mail',
        'product',
        'project',
        'purchase',
        'purchase_requisition',
        'sale',
        'sales_team',
        'stock',
        'survey',
        'web',
        'web_studio',
    ],
    'data': [
        'data/ir_model.xml',
        'data/ir_model_fields.xml',
        'data/ir_ui_view.xml',
        'data/ir_actions_act_window.xml',
        'data/ir_actions_report.xml',
        'data/mail_template.xml',
        'data/ir_actions_server.xml',
        'data/ir_ui_menu.xml',
        'data/base_automation.xml',
        'data/ir_model_access.xml',
    ],
    'application': False,
    'license': 'OPL-1',
}
