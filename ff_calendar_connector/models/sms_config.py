from odoo import fields, models


class SmsConfig(models.Model):
    _name = "sms.configuration"
    _rec_name = "username"

    username = fields.Char("Username")
    api_key = fields.Char("API Key")
