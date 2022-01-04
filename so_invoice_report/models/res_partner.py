# -*- coding: utf-8 -*-
from odoo import models, fields, api
from num2words import num2words
import math
import re
import uuid

class ResPartner(models.Model):
    _inherit = 'res.partner'

    fax = fields.Char(string="Fax")
    build_no = fields.Char(string="Build No")
    district = fields.Char(string="District")
    add_no = fields.Char(string="Additional No")
    value_registration_no = fields.Char(string="value registration number")
    other_id = fields.Char(string="Another id")

class AccountInvoiceLine(models.Model):
    _inherit = 'account.move.line'
    tax_value = fields.Float(string="Tax Value",compute='_get_tax_value')
    number = fields.Integer(compute='_compute_number', store=True)
    # day = fields.Selection([
    #     ('monday', 'Monday'),
    #     ('tuesday', 'Tuesday'),
    #     ('wednesday', 'Wednesday'),
    #     ('thursday', 'Thursday'),
    #     ('friday', 'Friday'),
    #     ('saturday', 'Saturday'),
    #     ('sunday', 'Sunday')
    #     ], 'Day of Week', index=True, default='sunday')
    

    @api.depends('sequence', 'move_id')
    def _compute_number(self):
        for invoice in self.mapped('move_id'):
            number = 1
            for line in invoice.invoice_line_ids:
                line.number = number
                number += 1

    def _get_tax_value(self):
        for record in self:
            record.tax_value = record.price_total - record.price_subtotal


class AccountInvoicEe(models.Model):
    _inherit = 'account.move'

    project = fields.Char(string="Project" )
    po_no = fields.Char(string="Po Number" )
    po_date = fields.Date('PO Date')
    total_price_without_disc = fields.Float(string="Total Price Without Disc",compute='_get_total_price' )
    validate_user_id = fields.Many2one(comodel_name="res.users", string="Approval User", required=False, )
    total_dis = fields.Float(compute='_compute_total_dis')
    @api.depends('invoice_line_ids')
    def _compute_total_dis(self):
        self.total_dis = self.total_price_without_disc - self.amount_untaxed


    def action_invoice_open(self):
        current_user = self.env.user
        for record in self :
            record.validate_user_id = current_user
        res = super(AccountInvoicEe, self).action_invoice_open()
        return res


    def _get_total_price(self):
        for record in self :
            record.total_price_without_disc = sum(line.price_unit * line.quantity for line in record.invoice_line_ids)

    def convertNumber_en(self, amountInt):
        result = num2words(amountInt, lang='en')
        return result

    def convertNumber_ar_split(self, numbers):
        finla_number = (numbers // 10 ** (int(math.log(numbers, 10)) - 3 + 1))
        result = num2words(finla_number, lang='ar')
        return result

    def convertNumber_ar(self, amountInt):
        result = num2words(amountInt, lang='ar')
        return result

    def action_invoice_open(self):
        current_user = self.env.user
        for record in self :
            record.validate_user_id = current_user
        res = super(AccountInvoicEe, self).action_invoice_open()
        return res


