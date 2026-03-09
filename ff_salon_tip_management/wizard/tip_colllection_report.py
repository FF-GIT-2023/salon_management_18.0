from odoo import fields, models
from datetime import datetime, time
import pytz


class TipReportWiz(models.TransientModel):
    _name = "tip.report.wiz"
    _description = "Tip Report generation wizard"

    date_from = fields.Date()
    date_to = fields.Date()
    user_id = fields.Many2one("res.users", string="Technician")

    def get_records(self):
        user_tz = pytz.timezone(self.env.user.tz or "UTC")

        start_dt = user_tz.localize(datetime.combine(self.date_from, time.min))
        end_dt = user_tz.localize(datetime.combine(self.date_to, time.max))

        date_from = start_dt.astimezone(pytz.UTC).replace(tzinfo=None)
        date_to = end_dt.astimezone(pytz.UTC).replace(tzinfo=None)

        domain = [
            ("create_date", ">=", date_from),
            ("create_date", "<=", date_to),
        ]

        if self.user_id:
            domain.append(("user_id", "=", self.user_id.id))

        return self.env["salon.tip"].search(domain)

    def generate_report(self):
        records = self.get_records()
        return self.env.ref(
            "ff_salon_tip_management.work_tip_report"
        ).report_action(records)

    def print_xlsx_report(self):
        return self.env.ref(
            "ff_salon_tip_management.action_report_tip_collection_report_xlsx"
        ).report_action(self)
