# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # def _default_branch_id(self):
    #     branch_id = self.env['res.users'].browse(self._uid).branch_id.id
    #     return branch_id

    def get_domain(self):
        return [('id', 'in', self.env.user.branch_ids.ids)]

    branch_id = fields.Many2one('res.branch',domain=get_domain)