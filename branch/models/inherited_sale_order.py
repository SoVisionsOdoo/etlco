# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # @api.constrains('branch_id')
    # def constrain_branch(self):
    #     if self.branch_id.company_id.id != self.company_id.id:
    #         raise UserError(_('You should select Branch in the same company sale order'))

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    def get_domain(self):
        return [('id', 'in', self.env.user.branch_ids.ids)]
    
    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)
        user_branch = self.env['res.users'].browse(self.env.uid).branch_id
        if user_branch:
            branched_warehouse = self.env['stock.warehouse'].search([('branch_id', '=', user_branch.id)])
            if branched_warehouse:
                res['warehouse_id'] = branched_warehouse.ids[0]
            else:
                res['warehouse_id'] = False

        return res

    branch_id = fields.Many2one('res.branch', default=_default_branch_id,domain=get_domain)

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res['branch_id'] = self.branch_id.id
        return res

    @api.onchange('branch_id')
    def onchange_branch_id(self):
        self.analytic_account_id = self.branch_id.analytic_account_id.id
        self.warehouse_id = self.env['stock.warehouse'].search([('branch_id','=',self.branch_id.id)],limit=1).id


class SaleOrderline(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line(self):
        self.ensure_one()
        res = super(SaleOrderline, self)._prepare_invoice_line()
        res['branch_id'] = self.order_id.branch_id.id
        return res
