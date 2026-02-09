{
    "name": "Walk In Customer Bookings",
    "version": "18.0.1.0.0",
    "summary": "Information about walk in customers bookings",
    "category": "Point Of Sale",
    "author": "ForeFront Technologies",
    "depends": ["base", "point_of_sale", "ff_calendar_connector"],
    "data": [
        "security/ir.model.access.csv",
        "security/booking_groups.xml",
        "views/menu.xml",
        "views/walk_in_customers.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "auto_install": False,
    "application": False,
}
