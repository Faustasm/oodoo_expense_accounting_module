from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, AccessDenied
from datetime import datetime
from .base import BaseModel


class Expense(BaseModel):

    _name = "eam.expense"
    status = fields.Selection(
        [("confirmed", "Confirmed"), ("unconfirmed", "Unconfirmed")], string="Status"
    )

    @api.constrains("date_from", "date_to", "category")
    def _update_statuses(self):
        current_date = datetime.today().strftime("%Y-%m-%d")
        budget_records = (
            self.sudo()
            .env["eam.budget"]
            .search(
                [
                    ("date_from", "<=", current_date),
                    ("date_to", ">=", current_date),
                    ("category", "=", self.category),
                ]
            )
        )
        if budget_records:
            # If expense amount does not exceed 5 percent of budget confirm automatically
            allowed_budget = budget_records[0]
            if self.converted_amount > allowed_budget.converted_amount:
                raise ValidationError("Expense exceeds budget amount")
            if self.converted_amount < allowed_budget.converted_amount / 100 * 5:
                self.status = "confirmed"
            else:
                self.status = "unconfirmed"
        else:
            raise ValidationError("No budget for expense found.")

    def action_confirm(self):
        manager_group = self.env.ref("expense_accounting_module.group_expense_managers")
        admin_group = self.env.ref("expense_accounting_module.group_expense_admins")
        if (
            manager_group not in self.env.user.groups_id
            and admin_group not in self.env.user.groups_id
        ):
            raise AccessDenied("You are not authorized to change the status.")
        else:
            title_string = ""
            message_string = ""
            message_type = ""
            for rec in self:
                if rec.status == "unconfirmed":
                    rec.status = "confirmed"
                    title_string = "Success!"
                    message_string = "Expense confirmed!"
                    message_type = "success"
                else:
                    title_string = "Warning!"
                    message_string = "Expense was already confirmed!"
                    message_type = "danger"
            title = _(title_string)
            message = _(message_string)
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": title,
                    "message": message,
                    "type": message_type,
                    "sticky": False,
                },
            }
