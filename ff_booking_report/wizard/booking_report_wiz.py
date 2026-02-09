from odoo import api, fields, models
from odoo.exceptions import UserError


class BookingReportWizard(models.TransientModel):
    _name = "booking.report.wiz"
    _description = "Booking Report Wizard"

    start_date = fields.Date(string="Start Date", default=fields.Date.today)
    end_date = fields.Date(string="End Date", default=fields.Date.today)
    status = fields.Selection(
        [
            ("pending", "Pending"),
            ("confirm", "Confirmed"),
            ("cancel", "Cancelled"),
            ("removed", "Removed"),
        ],
        string="Status",
        default="confirm",
        required=True,
    )

    company_ids = fields.Many2many(
        "res.company", string="Company", default=lambda self: self.env.company
    )

    all_location = fields.Boolean(string="All Location", default=False)

    @api.onchange("all_location")
    def _onchange_all_location(self):

        if self.all_location:
            self.company_ids = self.env["res.company"].search([])
        else:
            self.company_ids = self.env.company

    def action_generate_report(self):
        domain = []
        if self.start_date > self.end_date:
            raise UserError("Start Date cannot be after End Date.")
        if self.start_date:
            domain += [("create_date", ">=", self.start_date)]
        if self.end_date:
            domain += [("create_date", "<=", self.end_date)]
        if self.company_ids:
            domain += [("company_id", "in", self.company_ids.ids)]

        domain += [("state", "=", self.status)]

        calendar_event = self.env["calendar.event"].search_read(domain)

        if not calendar_event:
            raise UserError("No bookings found for the selected criteria.")

        company_wise_data = {}
        for booking in calendar_event:
            company_key = booking.get("company_id")[0]
            if company_key not in company_wise_data:
                company_wise_data[company_key] = {
                    "company_name": booking.get("company_id")[1],
                    "records": [],
                }
            company_wise_data[company_key]["records"].append(booking)

        return self.env.ref(
            "ff_booking_report.booking_report_action_pdf"
        ).report_action(
            None,
            data={
                "company_wise_data": company_wise_data,
                "start_date": self.start_date.strftime("%d/%m/%Y"),
                "end_date": self.end_date.strftime("%d/%m/%Y"),
            },
        )
