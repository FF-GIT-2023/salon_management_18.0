from odoo import models


class TipReportXslx(models.AbstractModel):
    _name = "report.ff_salon_tip_management.tip_report_xlsx"
    _description = "Tip Collection Report XLSX Report"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, collections_data, lines):
        selection_value = {"not_paid": "Not Paid", "paid": "Paid"}
        sheet = workbook.add_worksheet("Tip Collection Report")
        bold = workbook.add_format({"bold": True})
        sheet.merge_range(3, 3, 0, 11, "Technician Tip Collection Report", bold)
        sheet.write(7, 0, "Rec Name", bold)
        sheet.write(7, 2, "Technician Name", bold)
        sheet.write(7, 4, "Amount", bold)
        sheet.write(7, 6, "Status", bold)
        row = 9
        tip_details = lines.get_records()
        for data in tip_details:
            sheet.write(row, 0, data.name or "")
            sheet.write(row, 2, data.user_id.name or "")
            sheet.write(row, 4, data.amount or "")
            sheet.write(row, 6, selection_value[data.state] or "")
            row += 1
