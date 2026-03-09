from odoo import api, fields, models


class SaleTipPayWiz(models.TransientModel):
    _name = "sale.tip.pay.wiz"
    _description = "Sale Tip Pay"

    user_id = fields.Many2one("res.users", string="Sales Person")
    tot_amount = fields.Monetary(string="Total Tip")

    tip_line_ids = fields.Many2many(
        "salon.tip",
        string="Tips"
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id.id,
    )

    @api.onchange("user_id")
    def _get_tip_lines(self):
        self.tip_line_ids = [(6, 0, [])]

        if self.user_id:
            rec_lst = []
            tips = self.env["salon.tip"].search([
                ("state", "=", "not_paid"),
                ("user_id", "=", self.user_id.id)
            ])

            for tip in tips:
                rec_lst.append((4, tip.id))

            self.tip_line_ids = rec_lst

    def pay_salon_user_tips(self):
        for tip in self.tip_line_ids:
            tip.state = "paid"
