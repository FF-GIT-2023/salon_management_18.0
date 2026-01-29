from odoo import api, fields, models


class WorkerSchedule(models.Model):
    _name = "worker.schedule"
    _description = "Schedule Weekly Work"
    _order = "name, id"

    name = fields.Char(
        readonly=True,
        required=True,
        copy=False,
        default=lambda self: self.env["ir.sequence"].next_by_code("worker.schedule"),
    )
    start_date = fields.Datetime(required=True)
    end_date = fields.Datetime(required=True)
    user_id = fields.Many2one("res.users", string="Technician")
    state = fields.Selection(
        [
            ("not_scheduled", "Not Scheduled"),
            ("scheduled", "Scheduled"),
            ("request_off", "Requested Off"),
        ],
        required=True,
        default="not_scheduled",
        string="Scheduler State",
    )
    time = fields.Float(
        string="Total Hours", compute="_compute_hours_from_dates", store=True
    )

    @api.depends("start_date", "end_date")
    def _compute_hours_from_dates(self):
        for rec in self:
            rec.time = 0.0
            if rec.start_date and rec.end_date:
                time_diff = rec.end_date - rec.start_date
                rec.time = float(time_diff.total_seconds() / 3600)
