from odoo import fields, models


class User(models.Model):
    _inherit = "res.partner"
    expense_ids = fields.Many2many("eam.expense", string="Teams")
