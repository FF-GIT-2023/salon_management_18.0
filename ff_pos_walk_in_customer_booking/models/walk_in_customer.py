from odoo import _, api, fields, models
from odoo.exceptions import UserError


class WalkInCustomer(models.Model):
    _name = "walk.in.customer"
    _rec_name = "partner_id"

    partner_id = fields.Many2one("res.partner", string="Name")
    phone = fields.Char("Phone No", required=True)
    email = fields.Char("E-mail", required=True)
    note = fields.Text("Notes")
    service_ids = fields.Many2many(
        "product.product",
        string="Service",
        domain="[('available_in_pos', '=', True),"
        "('sale_ok', '=', True), ('type', '=', 'service')]",
    )
    user_id = fields.Many2one("res.users", string="Stylist Name")
    check_in_time = fields.Datetime(string="Time-in")
    check_out_time = fields.Datetime(string="Time-out")
    check_in_bool = fields.Boolean("Time-in Boolean", default=False)
    check_out_bool = fields.Boolean("Time-out Boolean", default=False)
    created_date = fields.Datetime(string="Create Date", default=fields.Datetime.now)
    service_state = fields.Selection(
        [
            ("waiting", "Waiting"),
            ("on_hold", "On Hold"),
            ("under_service", "Under Service"),
            ("completed", "Completed"),
            ("cancel", "Cancelled"),
        ],
        string="Service Status",
        default="waiting",
        group_expand="_group_expand_states",
        track_visibility="always",
    )
    company_id = fields.Many2one(
        "res.company",
        string="Location",
        required=True,
        default=lambda self: self.env.company,
    )

    @api.onchange("company_id")
    def _onchange_company_id(self):
        for rec in self:
            return {"domain": {"user_id": [("company_id.id", "=", rec.company_id.id)]}}

    def on_hold(self):
        self.write(
            {
                "service_state": "on_hold",
            }
        )

    def action_cancel(self):
        self.write(
            {
                "service_state": "cancel",
            }
        )

    def go_for_service(self):
        self.write(
            {
                "service_state": "under_service",
            }
        )

    def service_done(self):
        self.write(
            {
                "service_state": "completed",
            }
        )

    def action_check_in(self):
        self.check_in_bool = True
        self.write({"check_in_time": fields.Datetime.now()})

    def action_check_out(self):
        self.check_out_bool = True
        self.write({"check_out_time": fields.Datetime.now()})

    def _group_expand_states(self, states, domain):
        return [key for key, val in type(self).service_state.selection]
