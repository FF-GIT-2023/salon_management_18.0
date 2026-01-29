from odoo import models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def action_send_mail(self):
        res = super().action_send_mail()

        event_id = self.env.context.get("booking_confirm_event_id")
        if event_id:
            event = self.env["calendar.event"].browse(event_id)
            event.write({
                "state": "confirm",
                "active_user": self.env.user.name,
            })

        return res
