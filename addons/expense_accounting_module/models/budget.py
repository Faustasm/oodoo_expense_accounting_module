from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from .base import BaseModel


class Budget(BaseModel):

    _name = 'eam.budget'
    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)
     
    @api.constrains('category', 'date_from', 'date_to')
    def _check_unique_category_date(self):
        record_ids = [record.id for record in self]
        existing_budget = self.search([
            ('id', 'not in', record_ids),
            ('category', '=', self.category),
            ('date_from', '<=', self.date_to),
            ('date_to', '>=', self.date_from)
        ])
        
        if existing_budget:
            raise ValidationError("Budget with this category already exists within the selected date range.")
