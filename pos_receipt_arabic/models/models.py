# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class POSConFig(models.Model):
    _inherit = 'pos.config'

    allow_qr_code = fields.Boolean(string="Add QR Code in Receipt")
        



