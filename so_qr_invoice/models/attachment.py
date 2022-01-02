
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class Attachment(models.Model):
    _name = "so_qr_invoice.attachment"
    _inherit = 'ir.attachment'

    attach_model = fields.Char(string='Report Model', required=True)
    attach_type = fields.Char(string='Report Type', required=True)