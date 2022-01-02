from odoo import api, fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    branch_id = fields.Many2one('res.branch', 'Branch')

    @api.onchange('type')
    def onchange_type(self):
        if self.type not in ['cash', 'bank']:
            self.branch_id = False
