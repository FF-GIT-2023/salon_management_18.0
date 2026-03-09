{
    "name": "Salon Tip Management",
    "version": "18.0.1.0.0",
    "summary": "Salon User Tip Management",
    "category": "Point of Sale",
    "author": "ForeFront Technologies",
    "depends": [
        "point_of_sale",
        "hr",
        "report_xlsx",
        "salesperson_pos_order_line"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/salon_tip_view.xml",
        "wizard/sale_tip_pay_wiz.xml",
        "wizard/tip_collection_report_view.xml",
        "reports/reports.xml",
        "reports/work_schedule_report.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": True,
}
