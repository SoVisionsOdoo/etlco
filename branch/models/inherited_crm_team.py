from odoo import api, fields, models

class CrmTeam(models.Model):
    _inherit = 'crm.team'

    branch_id = fields.Many2one('res.branch','Branch')

