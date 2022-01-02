# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_domain(self):
        return [('id', 'in', self.env.user.branch_ids.ids)]

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    branch_id = fields.Many2one('res.branch',deafult=_default_branch_id, domain=get_domain, )

    @api.onchange('branch_id')
    def _onchange_branch_id(self):
        for move in self:
            for line in move.line_ids:
                line.branch_id = move.branch_id.id

    # def _recompute_dynamic_lines(self, recompute_all_taxes=False):
    #     res = super(AccountMove, self)._recompute_dynamic_lines(recompute_all_taxes=recompute_all_taxes)
    #     self._onchange_branch_id()
    #     return res


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    branch_id = fields.Many2one('res.branch', related='move_id.branch_id', store=True, readonly=True)


# class Asset(models.Model):
#     _inherit = 'account.asset'
#
#     def get_domain(self):
#         return [('id', 'in', self.env.user.branch_ids.ids)]
#
#     def _default_branch_id(self):
#         branch_id = self.env['res.users'].browse(self._uid).branch_id.id
#         return branch_id
#
#     branch_id = fields.Many2one('res.branch', default=_default_branch_id, domain=get_domain, )
