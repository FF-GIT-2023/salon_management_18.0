from odoo import fields, models


class SAlonTipWiz(models.TransientModel):
    _name = "salon.tip.management.report.wiz"
    _description = "Tip Management Wizard"

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    sales_man = fields.Many2one("res.users")

    def tip_print_report(self):
        return
