import logging
from ast import literal_eval

import clicksend_client
import pytz
from clicksend_client import SmsMessage
from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CalendarEvent(models.Model):
    _inherit = "calendar.event"
    _rec_name = "customer_id"

    @api.model
    def _default_partners(self):
        partners = self.env.user.partner_id
        if self.customer_id != partners.ids:
            return self.customer_id
        return partners

    state = fields.Selection(
        [
            ("pending", "Pending"),
            ("confirm", "Confirmed"),
            ("cancel", "Cancelled"),
            ("removed", "Removed"),
        ],
        "Status",
        copy=False,
        tracking=True,
        group_expand="_group_expand_states",
        default="pending",
    )
    user_id = fields.Many2one("res.users", string="Staff")
    customer_id = fields.Many2one("res.partner", string="Customer", required=True)
    mail = fields.Char(string="E-mail", required=True)
    phone_no = fields.Char(string="Phone No:")
    note = fields.Text(string="Notes")
    location = fields.Many2one(
        "res.company", readonly=False, related="user_id.company_id"
    )
    ms_booking_reference = fields.Char("Booking Reference")
    company_id = fields.Many2one("res.company", "Company", related="user_id.company_id")
    active_user = fields.Char("Confirmed By")
    removed_by = fields.Char("Removed By")
    removed_on = fields.Char("Removed On")
    partner_ids = fields.Many2many(
        "res.partner",
        "calendar_event_res_partner_rel",
        string="Attendees",
        default=_default_partners,
    )

    @api.onchange("location")
    def _onchange_location(self):
        for rec in self:
            return {"domain": {"user_id": [("company_id.id", "=", rec.location.id)]}}

    def action_confirm(self):
        template = self.env.ref("ff_calendar_connector.booking_status_email_template")
        compose_form = self.env.ref("mail.email_compose_message_wizard_form")
        ctx = {
            "default_model": "calendar.event",
            "default_res_ids": self.ids,
            "default_use_template": bool(template),
            "default_template_id": template.id,
            "default_composition_mode": "comment",
            "default_email_from": self.company_id.email,
            "default_email_to": self.mail,
            "default_subject": "Booking Status",
            "booking_confirm_event_id": self.id,
        }
        # -------------------------------sms sending process-------------------------------------------#
        sms_conf_obj = self.env["sms.configuration"].search([])
        for sms_cred in sms_conf_obj:
            username = sms_cred.username
            password = sms_cred.api_key
            if not username or not password:
                raise UserError(
                    _("Please configure your SMS Configuration credentials")
                )
            configuration = clicksend_client.Configuration()
            configuration.username = username
            configuration.password = password

            number = False
            api_instance = clicksend_client.SMSApi(
                clicksend_client.ApiClient(configuration)
            )
            if not self.phone_no:
                raise UserError(_("Please provide the Phone number"))
            else:
                number = self.phone_no
            if number:
                sms_message = SmsMessage(
                    source="php",
                    body="Your booking is confirmed.",
                    to=number,
                    schedule=1436874701,
                )
                sms_messages = clicksend_client.SmsMessageCollection(
                    messages=[sms_message]
                )
                try:
                    api_response = api_instance.sms_send_post(sms_messages)
                    response = api_response.replace("'", '"')
                    response = literal_eval(response)
                    if response.get("response_code") == "SUCCESS":
                        pass
                    else:
                        pass
                except Exception as e:
                    _logger.warning(
                        "Exception when calling SMSApi->sms_send_post: %s\n" % e
                    )
        return {
            "name": template.name,
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form.id, "form")],
            "view_id": compose_form.id,
            "target": "new",
            "context": ctx,
        }

    def action_cancel(self):
        self.write({"state": "cancel"})

    def action_set_to_pending(self):
        self.write({"state": "pending"})

    def _group_expand_states(self, states, domain):
        return [key for key, val in type(self).state.selection]

    def unlink(self):
        for rec in self:
            rec.write(
                {
                    "state": "removed",
                    "removed_by": self.env.user.name,
                    "removed_on": fields.Datetime.now(),
                    "active": False,
                }
            )
            rec.message_post(body=f"This record was removed by {self.env.user.name}")
        return True

    def get_local_start_time(self):
        user_tz = pytz.timezone(self.env.context.get("tz") or self.env.user.tz)
        start = pytz.utc.localize(self.start).astimezone(user_tz)
        return start.strftime("%I:%M %p")
