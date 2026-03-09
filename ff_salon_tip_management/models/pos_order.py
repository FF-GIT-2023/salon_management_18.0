from odoo import api, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def create(self, vals):
        order = super().create(vals)

        for line in order.lines:
            if line.tip_amount and line.tip_amount > 0:
                self.env["salon.tip"].create({
                    "user_id": line.product_id.pos_sales_person_id.id or self.env.user.id,
                    "amount": line.tip_amount,
                    "state": "not_paid",
                    "order_reference": order.pos_reference,
                })

        return order


