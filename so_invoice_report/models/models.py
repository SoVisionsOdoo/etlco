# -*- coding: utf-8 -*-
from odoo import _, api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'
    name_arbic = fields.Char(string="Company Arabic Name",)
    header = fields.Binary(string="Header Image",)
    footer = fields.Binary(string="Footer Image",)
    banck_account_name = fields.Char(string="Bank Account Name",)
    banck_name = fields.Char(string="Bank Name",)
    banck_name_ar = fields.Char(string="Bank Name Arabic",)
    bank_address = fields.Char(string="Bank Address",)
    banck_account_no = fields.Char(string="Bank Account NO",)
    iban = fields.Char(string="IBAN",)
    swift = fields.Char(string="Swift No",)
    # invoice_design = fields.Selection(selection=[
    #     ('1', 'شركة ابهار الحركة للديكور (شركة شخص واحد )'),
    #     ('2', 'شركة ابهار الكلم لتنظيم المعارض والمؤتمرات (شركة شخص واحد )'),
    #     ('3', 'قطاع المنسوجات للزي الموحد'),
    #     ('4', 'مؤسسة ابهار فومي للمقاولات'),
    #     ]
    # ,string='Invoice Design',required=True)


