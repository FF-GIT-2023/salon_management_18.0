from odoo import fields, models


class SchedulerReportWiz(models.Model):
    _name = "scheduler.report.wiz"
    _description = "Report generation wizard"

    date_from = fields.Date()
    date_to = fields.Date()

    def _prepare_report_data(self):
        records = self.get_records()
        report_obj = self.env["ir.actions.report"]
        report = report_obj._get_report_from_name(
            "ff_salon_worker_schedule.work_schedule_report_template"
        )
        data = {"doc_model": report.model, "docs": records}
        return data

    def get_records(self):
        return self.env["worker.schedule"].search(
            [("start_date", ">=", self.date_from), ("end_date", "<=", self.date_to)]
        )

    def generate_report(self):
        self.ensure_one()
        data = self._prepare_report_data()
        action = self.env.ref(
            "ff_salon_worker_schedule.work_schedule_report"
        ).report_action(data["docs"].ids)
        return action

    def print_scheduler_xls(self):
        return self.env.ref(
            "ff_salon_worker_schedule.action_report__work_schedule_report_xlsx"
        ).report_action(self)
