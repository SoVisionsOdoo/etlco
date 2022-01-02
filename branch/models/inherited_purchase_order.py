# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class purchase_order(models.Model):
    _inherit = 'purchase.order.line'

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    branch_id = fields.Many2one('res.branch', related='order_id.branch_id', default=_default_branch_id)

    def _create_stock_moves(self, picking):
        moves = self.env['stock.move']
        done = self.env['stock.move'].browse()
        for line in self:
            for val in line._prepare_stock_moves(picking):
                val.update({
                    'branch_id': line.branch_id.id,
                })

                done += moves.create(val)
        return done


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # @api.constrains('branch_id')
    # def constrain_branch(self):
    #     if self.branch_id.company_id.id != self.company_id.id:
    #         raise UserError(_('You should select Branch in the same company purchase order'))

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    def get_domain(self):
        return [('id', 'in', self.env.user.branch_ids.ids)]

    @api.onchange('branch_id')
    def onchange_branch_id(self):
        self.picking_type_id = self.env['stock.picking.type'].search(
            [('warehouse_id.branch_id', '=', self.branch_id.id), ('code', '=', 'incoming')], limit=1).id

    @api.model
    def default_get(self, fields):
        res = super(PurchaseOrder, self).default_get(fields)
        user_branch = self.env['res.users'].browse(self.env.uid).branch_id
        if user_branch:
            branched_warehouse = self.env['stock.warehouse'].search([('branch_id', '=', user_branch.id)])
            if branched_warehouse:
                res['picking_type_id'] = branched_warehouse[0].in_type_id.id
            else:
                res['picking_type_id'] = False
        else:
            res['picking_type_id'] = False
        return res

    branch_id = fields.Many2one('res.branch', default=_default_branch_id,domain=get_domain)

    @api.model
    def _prepare_picking(self):
        res = super(PurchaseOrder, self)._prepare_picking()
        res['branch_id'] = self.branch_id.id
        return res

    def action_view_invoice(self):
        result = super(PurchaseOrder, self).action_view_invoice()
        result['context']['default_branch_id'] = self.branch_id.id
        return result
