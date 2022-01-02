# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    branch_id = fields.Many2one('res.branch')

    @api.model
    def _select(self):
        return super(AccountInvoiceReport, self)._select() + ", line.branch_id as branch_id"