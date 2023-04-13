import uuid
from odoo import fields, models, api
from datetime import datetime, timedelta


class ProjektiReservations(models.Model):
    _name = 'projekti.reservations'
    _description = 'Description'
    _rec_name = 'reservation_code'

    reservation_code = fields.Char(string='Reservation Code',required=True, readonly=True,
                                   default=lambda self: str(uuid.uuid4()))
    res_date = fields.Datetime(string='Reservation date', required=False, default=lambda self: fields.datetime.now())
    check_in = fields.Datetime(string='Check in',  required=False)
    check_out = fields.Datetime(string='Check out', required=False)
    no_nights = fields.Integer(string='Number of nights',  required=False, compute='_compute_no_nights')
    total_price = fields.Float(string='Total price',  required=False, compute='_compute_total_price')
    adults = fields.Integer(string='Adults', required=False)
    children = fields.Integer(string='Children', required=False)
    res_type = fields.Selection(string='Reservation Type ', required=False,
                                selection=[('agency', 'Agency'),
                                           ('booking', 'Booking'),
                                           ('website', 'Website'),
                                           ('phone', 'Phone'),
                                           ])
    state = fields.Selection(string='State', required=False, default='draft',
                             selection=[('draft', 'Draft'),
                                        ('done', 'Confirmed'),
                                        ('cancel', 'Canceled'),
                                        ])
    special_requirements = fields.Text(string="Special requirements", required=False)
    points = fields.Integer(string='Loyalty Points', default=100)
    customer_id = fields.Many2one(comodel_name='projekti.customer', string='Customer', required=True)
    hotel_id = fields.Many2one(comodel_name='projekti.hotels', string='Hotel', required=True)
    room_ids = fields.Many2many(comodel_name='projekti.rooms', string='Rooms', required=True)
    discount_percentage = fields.Float(string='Discount Percentage', compute='compute_discount_percentage')

    @api.onchange('hotel_id')
    def onchange_hotel_id(self):
        if self.hotel_id:
            domain = [('hotel_id', '=', self.hotel_id.id), ('status', '=', 'ready')]
        else:
            domain = [('id', '=', False)]
        return {'domain': {'room_ids': domain}}

    @api.depends('customer_id.discount_percentage')
    def compute_discount_percentage(self):
        for reservation in self:
            reservation.discount_percentage = reservation.customer_id.discount_percentage

    @api.onchange('total_price', 'discount_percentage')
    def onchange_total_price(self):
        self.total_price -= self.total_price * (self.discount_percentage / 100)

    @api.depends('check_in', 'check_out')
    def _compute_no_nights(self):
        for reservation in self:
            if reservation.check_in and reservation.check_out:
                check_in_str = reservation.check_in.strftime('%Y-%m-%d %H:%M:%S')
                check_out_str = reservation.check_out.strftime('%Y-%m-%d %H:%M:%S')
                check_in_dt = datetime.strptime(check_in_str, '%Y-%m-%d %H:%M:%S')
                check_out_dt = datetime.strptime(check_out_str, '%Y-%m-%d %H:%M:%S')
                reservation.no_nights = (check_out_dt - check_in_dt).days
            else:
                reservation.no_nights = 0

    @api.depends('room_ids.price', 'no_nights')
    def _compute_total_price(self):
        for reservation in self:
            total_price = sum(room.price for room in reservation.room_ids)
            total_price *= reservation.no_nights
            reservation.total_price = total_price

    @api.model
    def create(self, vals):
        reservation = super(ProjektiReservations, self).create(vals)
        for room in reservation.room_ids:
            room.write({'status': 'occupied'})
        return reservation

    def write(self, vals):
        if 'state' in vals:
            current_state = self.state
            new_state = vals['state']
            if current_state != new_state and new_state == 'done':
                for room in self.room_ids:
                    room.write({'status': 'occupied'})
        return super(ProjektiReservations, self).write(vals)

    def confirm(self):
        self.state = "done"

    def cancel(self):
        self.state = "cancel"

    def draft(self):
        self.state = "draft"

    @api.model
    def create(self, vals):
        reservation = super(ProjektiReservations, self).create(vals)
        reservation.customer_id.update_loyalty_points()
        return reservation


    # default=lambda self: '%s-%s' % (self.customer_id.name[:4].upper(), datetime.now().strftime('%y%m%d%H%M%S'))

    # def unlink(self):
    #     confirm = input('Are you sure you want to cancel this reservation? (Y/N)').lower()
    #     self.ensure_one()
    #     if confirm == 'y':
    #         self.state = 'done'
    #         return super(ProjektiReservations, self).unlink()
    #     else:
    #         return False

