import random
import re
import pytz
from odoo import http, fields
from odoo.http import request
from datetime import datetime, timedelta, time


class SalonWebsite(http.Controller):
    @http.route('/', website=True, auth="public")
    def home(self, **kw):
        return request.render("ff_salon_website.main_template")

    @http.route('/about', type='http', auth="public")
    def about(self, **kw):
        return request.render("ff_salon_website.about_template")

    @http.route('/services', type='http', auth="public")
    def services(self, **kw):
        return request.render("ff_salon_website.service_template")

    @http.route('/price', type='http', auth="public")
    def price(self, **kw):
        return request.render("ff_salon_website.price_template")

    @http.route('/contact', type='http', auth="public")
    def contact(self, **kw):
        return request.render("ff_salon_website.contact_template")

    @http.route('/team', type='http', auth="public")
    def team(self, **kw):
        return request.render("ff_salon_website.team_template")

    @http.route('/testimonial', type='http', auth="public")
    def testimonial(self, **kw):
        return request.render("ff_salon_website.testimonial_template")

    @http.route('/gallery', type='http', auth="public")
    def gallery(self, **kw):
        return request.render("ff_salon_website.gallery_template")

    @http.route('/appointment', type='http', auth="public")
    def appointment(self, **kw):
        services_obj = request.env['product.template'].sudo().search([('type','=', 'service')])
        location_obj = request.env['res.company'].sudo().search([])
        return request.render("ff_salon_website.appointment_template",{'services':services_obj, 'locations':location_obj})

    @http.route('/web/contact/confirm', website=True, auth="public")
    def contact_confirm(self, **kwargs):
        lead = request.env['crm.lead']
        dupe_lead = lead.sudo().search(
            ['|', ('phone', '=', kwargs.get('phone')), ('email_from', '=', kwargs.get('email'))])
        if not dupe_lead:
            crm_vals = {
                'name': kwargs.get('subject'),
                'email_from': kwargs.get('email'),
                'phone': kwargs.get('phone'),
                'description': kwargs.get('message'),
            }
            partner = request.env['res.partner']
            partner_vals = {
                'name': kwargs.get('name'),
                'email': kwargs.get('email'),
                'phone': kwargs.get('phone'),
            }
            new_partner = partner.sudo().create(partner_vals)

            crm_rec = lead.sudo().create(crm_vals)
            crm_rec.partner_id = new_partner.id
            return request.render("ff_salon_website.contact_confirm_template")
        else:
            crm_vals = {
                'name': kwargs.get('subject'),
                'email_from': kwargs.get('email'),
                'phone': kwargs.get('phone'),
                'description': kwargs.get('message')
            }
            generate_lead = lead.sudo().create(crm_vals)
            generate_lead.partner_id = dupe_lead.partner_id.id
            return request.render("ff_salon_website.contact_confirm_template")

    @http.route('/customer/signup', type='http', website=True, auth="public")
    def customer_signup(self, **kwargs):
        location_obj = request.env['res.company'].sudo().search([])
        return request.render("ff_salon_website.signup_template",{'location':location_obj})

    @http.route('/confirm/signup', auth="public", website=True, type='http')
    def confirm_signup(self, **kwargs):
        user_obj = request.env['res.users'].sudo().search(['|', ('name', '=', kwargs.get('name')),
                                                           ('login', '=', kwargs.get('email'))])
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.#_\-])[A-Za-z\d@$!%*?&.#_\-]{8,}$'

        flag = False
        if (len(kwargs.get('password')) and len(kwargs.get('confirm_password'))) != 8:
            flag = True
            if flag:
                values = {
                    'incorrectformat': bool(flag),
                }
                return request.render("ff_salon_website.signup_template", values)
        elif not re.match(pattern, kwargs.get('password')):
            flag = True
            if flag:
                values = {
                    'incorrectformat': bool(flag),
                }
                return request.render("ff_salon_website.signup_template", values)
        if user_obj:
            values = {
                'show_user_popup': bool(user_obj),
            }
            return request.render("ff_salon_website.signup_template", values)
        partner_vals = {
            'name': kwargs.get('name'),
            'email': kwargs.get('email'),
            'phone': kwargs.get('phone'),
        }
        customer_obj = request.env['res.partner'].sudo().create(partner_vals)
        location_id = request.env['res.company'].sudo().search([('id','=',int(kwargs.get('location_id')))])
        user_vals = {
            'name':kwargs.get('name'),
            'login':kwargs.get('email'),
            'password': kwargs.get('confirm_password'),
            'partner_id':customer_obj.id,
            'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
            'company_ids': [(6, 0, location_id.ids)],
            'company_id': location_id.id,
        }
        user_obj = request.env['res.users'].sudo().create(user_vals)
        return request.render("ff_salon_website.signup_confirm_template")

    @http.route('/appointment/bookings', type='http', auth="public", website=True)
    def appointment_booking(self, **kwargs):
        bookings_obj = request.env['calendar.event']
        customer_obj = request.env['res.partner'].sudo().search(['&',('name','ilike',kwargs.get('name')),
                                                          ('email','=',kwargs.get('email'))], limit=1)
        if not customer_obj:
            partner = request.env['res.partner']
            partner_vals = {
                'name': kwargs.get('name'),
                'email': kwargs.get('email'),
                'phone': kwargs.get('phone'),
            }
            customer_obj = partner.sudo().create(partner_vals)

        service_id = int(kwargs.get('service'))
        location_id = int(kwargs.get('location_id'))
        date_time = kwargs.get('date_time')
        user_id = request.env['res.users'].search(['&',('name','=',kwargs.get('name')),('login','=',kwargs.get('email'))])
        if not user_id:
            values = {
                'show_user_popup': not bool(user_id),
            }
            return request.render("ff_salon_website.appointment_template", values)
        tz = pytz.timezone(request.env.user.tz or "UTC")
        start_dt = tz.localize(datetime.strptime(date_time, '%Y-%m-%dT%H:%M'))
        start_utc = start_dt.astimezone(pytz.utc)
        stop_utc = start_utc + timedelta(minutes=30)
        users_ids = request.env['res.users'].sudo().search([('company_ids', 'in', location_id),
                                                            ('groups_id', 'in',
                                                             [request.env.ref('base.group_user').id])])
        booking_rec = request.env['calendar.event'].sudo().search([('location','=',location_id),('start','>=',start_utc.date()),
                                                                   ('stop', '<=',start_utc.date())])
        user_assign = ''
        user_any = ''
        if booking_rec:
            user_list = []
            for rec in booking_rec:
                user_list.append(rec.user_id.id)
            for rec in booking_rec:
                if rec.start.time() <= start_utc.time() and rec.stop.time() > start_utc.time():
                    for user in users_ids:
                        if user.id not in user_list:
                            user_assign = user
                    if not user_assign:
                        services_obj = request.env['product.template'].sudo().search([('type', '=', 'service')])
                        location_obj = request.env['res.company'].sudo().search([])
                        values = {
                            'services': services_obj,
                            'locations': location_obj,
                            'show_popup': not bool(user_assign),
                            'popup_message': 'No staff available for selected time slot.',
                        }
                        return request.render("ff_salon_website.appointment_template", values)
                else:
                    user_assign = random.choice(users_ids)
        else:
            user_any = random.choice(users_ids)

        vals = {
            'name': request.env['product.template'].sudo().browse(service_id).name,
            'mail': kwargs.get('email'),
            'location': request.env['res.company'].sudo().browse(location_id),
            'customer_id': customer_obj.id,
            'start': fields.Datetime.to_string(start_utc),
            'stop': fields.Datetime.to_string(stop_utc),
            'user_id': user_assign.id if user_assign else user_any.id,
            'phone_no': kwargs.get('phone'),
        }
        bookings = bookings_obj.sudo().create(vals)
        return request.render("ff_salon_website.booking_confirm_template")

