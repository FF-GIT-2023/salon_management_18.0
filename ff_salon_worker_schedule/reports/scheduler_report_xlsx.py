import datetime

from odoo import models


class TipReportXslx(models.AbstractModel):
    _name = "report.ff_salon_worker_schedule.scheduler_report_xlsx"
    _description = "Work Schedule Report XLSX Report"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, collections_data, lines):
        selection_value = {
            "not_scheduled": "Not Scheduled",
            "scheduled": "Scheduled",
            "request_off": "Requested Off",
        }
        bold = workbook.add_format({"bold": True})
        sheet = workbook.add_worksheet("Employee Work Schedule Report")
        sheet.merge_range(3, 3, 0, 11, "Employee Work Schedule Report", bold)
        sheet.set_column(7, 0, 20)
        sheet.set_column(7, 2, 20)
        sheet.set_column(7, 4, 20)
        sheet.set_column(7, 6, 20)
        sheet.set_column(7, 8, 20)
        sheet.write(7, 0, "Technician Name", bold)
        sheet.write(7, 2, "Date Start", bold)
        sheet.write(7, 4, "Time Difference", bold)
        sheet.write(7, 6, "Date End", bold)
        sheet.write(7, 8, "Status", bold)
        row = 9
        tip_details = lines.get_records()
        for data in tip_details:
            date_start = datetime.datetime.strptime(
                str(data.start_date), "%Y-%m-%d %H:%M:%S"
            ).strftime("%d-%m-%Y %H:%M:%S")
            date_end = datetime.datetime.strptime(
                str(data.end_date), "%Y-%m-%d %H:%M:%S"
            ).strftime("%d-%m-%Y %H:%M:%S")
            sheet.write(row, 0, data.user_id.name or "")
            sheet.write(row, 2, date_start)
            sheet.write(
                row,
                4,
                "{:02.0f}:{:02.0f}".format(*divmod(float(data.time) * 60, 60)) or 0.0,
            )
            sheet.write(row, 6, date_end)
            sheet.write(row, 8, selection_value[data.state] or "")
            row += 1
