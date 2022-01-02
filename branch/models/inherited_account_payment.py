# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

MAP_INVOICE_TYPE_PARTNER_TYPE = {
    'out_invoice': 'customer',
    'out_refund': 'customer',
    'in_invoice': 'supplier',
    'in_refund': 'supplier',
}

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.model
    def default_get(self, default_fields):
        rec = super(AccountPayment, self).default_get(default_fields)
        active_ids = self._context.get('active_ids') or self._context.get('active_id')
        active_model = self._context.get('active_model')

        # Check for selected invoices ids
        if not active_ids or active_model != 'account.move':
            return rec

        invoices = self.env['account.move'].browse(active_ids).filtered(
            lambda move: move.is_invoice(include_receipts=True))
        rec['branch_id'] = invoices[0].branch_id.id
        return rec

    def get_domain(self):
        return [('id', 'in', self.env.user.branch_ids.ids)]

    branch_id = fields.Many2one('res.branch', 'Branch',domain=get_domain)

    def post(self):
        for payment in self:
            if payment.journal_id.branch_id.id not in self.env.user.branch_ids.ids:
                raise UserError( "You can not use this Payment Journal. Which is not in your branch")
        res = super(AccountPayment, self).post()
        return res