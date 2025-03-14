from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from currency_converter import CurrencyConverter


class BaseModel(models.Model):

    _name = 'eam.base'
    description = fields.Char(string='Description', required=True)
    amount = fields.Monetary(string='Amount', currency_field='currency_id', required=True)
    currency_id = fields.Many2one(
        'res.currency', 
        string='Currency', 
        required=True, 
        domain=[('name', 'in', ('USD', 'EUR'))]
    )
    converted_amount = fields.Monetary(string='Amount (USD)', currency_field='converted_amount_currency_id')
    converted_amount_currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        domain=[('name', 'in', ('USD'))]
    )
    category = fields.Selection([
        ('transportation', 'Transportation'),
        ('healthcare', 'Healthcare'),
        ('work_expense', 'Work expense')
    ], string='Category', required=True)

    user_id = fields.Many2one('res.users', string="Responsible", default=lambda s: s.env.user)
    team_ids = fields.Many2many('res.partner', string="Team")

    @api.constrains('amount', 'currency_id')
    def _update_converted_amount(self):
        converter = CurrencyConverter()
        self.converted_amount = converter.convert(self.amount, self.currency_id.name, 'USD')
        self.converted_amount_currency_id = self.sudo().env.ref('base.USD').id