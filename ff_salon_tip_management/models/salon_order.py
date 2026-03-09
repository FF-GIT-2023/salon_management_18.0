from odoo import fields, models


class SalonOrder(models.Model):
    _inherit = "salon.order"

    tip = fields.Monetary()
    chair_user = fields.Many2one(
        "res.users",
        default=lambda self: self.chair_id.user_id.id if self.chair_id else False,
    )

    def action_validate(self):
        res = super().action_validate()

        if self.tip:
            self.env["salon.tip"].create({
                "user_id": self.chair_user.id or self.chair_id.user_id.id,
                "amount": self.tip,
                "order_reference": self.name,
                "state": "not_paid",
            })

        return res
