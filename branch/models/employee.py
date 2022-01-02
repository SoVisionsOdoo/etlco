from odoo import api, fields, models, _
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import UserError, ValidationError


class HR(models.Model):
    _inherit = 'hr.employee'

    def get_domain(self):
        return [('id', 'in', self.env.user.branch_ids.ids)]

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    branch_id = fields.Many2one('res.branch', default=_default_branch_id, domain=get_domain, )


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.onchange('employee_id')
    def get_branch(self):
        self.branch_id = self.employee_id.branch_id.id

    branch_id = fields.Many2one('res.branch', )

    def action_payslip_done(self):
        res = super(HrPayslip, self).action_payslip_done()
        if self.move_id:
            self.move_id.branch_id = self.branch_id.id
        return res


class HRexpenses(models.Model):
    _inherit = 'hr.expense'

    def get_domain(self):
        return [('id', 'in', self.env.user.branch_ids.ids)]

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    branch_id = fields.Many2one('res.branch', default=_default_branch_id, domain=get_domain, )

    def action_submit_expenses(self):
        if any(expense.state != 'draft' or expense.sheet_id for expense in self):
            raise UserError(_("You cannot report twice the same line!"))
        if len(self.mapped('employee_id')) != 1:
            raise UserError(_("You cannot report expenses for different employees in the same report."))
        if any(not expense.product_id for expense in self):
            raise UserError(_("You can not create report without product."))

        todo = self.filtered(lambda x: x.payment_mode == 'own_account') or self.filtered(
            lambda x: x.payment_mode == 'company_account')
        return {
            'name': _('New Expense Report'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.expense.sheet',
            'target': 'current',
            'context': {
                'default_expense_line_ids': todo.ids,
                'default_company_id': self.company_id.id,
                'default_branch_id': self.branch_id.id,
                'default_employee_id': self[0].employee_id.id,
                'default_name': todo[0].name if len(todo) == 1 else ''
            }
        }

    def _get_account_move_by_sheet(self):
        """ Return a mapping between the expense sheet of current expense and its account move
            :returns dict where key is a sheet id, and value is an account move record
        """
        move_grouped_by_sheet = {}
        for expense in self:
            # create the move that will contain the accounting entries
            if expense.sheet_id.id not in move_grouped_by_sheet:
                move_vals = expense._prepare_move_values()
                move = self.env['account.move'].with_context(default_journal_id=move_vals['journal_id']).create(move_vals)
                move_grouped_by_sheet[expense.sheet_id.id] = move
            else:
                move = move_grouped_by_sheet[expense.sheet_id.id]
            move.branch_id = self.branch_id.id
        return move_grouped_by_sheet


class HRexpensesSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    def get_domain(self):
        return [('id', 'in', self.env.user.branch_ids.ids)]

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return branch_id

    branch_id = fields.Many2one('res.branch', default=_default_branch_id, domain=get_domain, )

