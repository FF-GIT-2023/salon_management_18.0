{
    "name": "Booking Report",
    "version": "18.0.1.0.0",
    "summary": "Booking report",
    "author": "ForeFront Technologies",
    "depends": ["base", "ff_pos_walk_in_customer_booking", "web"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/booking_report_wiz.xml",
        "reports/booking_report_template.xml",
        "reports/booking_report_action.xml",
    ],
    "license": "LGPL-3",
    "images": [],
    "installable": True,
    "auto_install": False,
    "application": True,
}
