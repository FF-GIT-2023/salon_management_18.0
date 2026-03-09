from odoo import _, api, fields, models


class SalonTipManagement(models.Model):
    _name = "salon.tip"
    _description = "Tip Payment Data"
    _rec_name = "name"

    name = fields.Char(
        required=True,
        readonly=True,
        default=lambda self: _("New"),
    )

    employee_id = fields.Many2one("hr.employee", string="Employee")

    amount = fields.Monetary()
    state = fields.Selection(
        [("not_paid", "Not Paid"), ("paid", "Paid")],
        default="not_paid",
    )

    user_id = fields.Many2one(
        "res.users",
        string="Stylist",
        required=True,
    )

    currency_id = fields.Many2one(
        "res.currency",
        required=True,
        default=lambda self: self.env.company.currency_id.id,
    )

    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
    )

    order_reference = fields.Char("Order Reference", required=True)

    @api.model
    def create(self, vals):
        if vals.get("name", _("New")) == _("New"):
            vals["name"] = self.env["ir.sequence"].next_by_code("salon.tip") or _("New")
        return super().create(vals)
