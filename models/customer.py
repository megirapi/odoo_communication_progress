
from odoo import fields, models, api


class ProjektiCustomer(models.Model):
    _name = 'projekti.customer'
    _description = 'Description'

    name = fields.Char(string=" Firstname/Lastname", required=True)
    address = fields.Char(string='Address', required=False)
    tel = fields.Char(string='Tel', required=True)
    gender = fields.Selection(string='Gender', required=True,
                              selection=[('female', 'Female'),
                                         ('male', 'Male'),
                                         ])
    country = fields.Char(string='Country', required=False)            
    postcode = fields.Char(string='Postcode',  required=False)
    review_ids = fields.One2many(comodel_name='projekti.review', inverse_name='customer_id', string='Reviews')
    num_reviews = fields.Integer(string="Number of Reviews", compute="_compute_num_reviews")
    reservation_ids = fields.One2many(comodel_name='projekti.reservations', inverse_name='customer_id',
                                      string='Reservations')
    num_reservations = fields.Integer(string="Number of Reservations", compute="_compute_num_reservations")
    loyalty_points = fields.Integer(string='Loyalty Points', compute='_compute_loyalty_points')
    discount_percentage = fields.Float(string='Discount',  required=False, compute='calculate_discount')

    @api.depends('review_ids')
    def _compute_num_reviews(self):
        for rec in self:
            rec.num_reviews = len(rec.review_ids)

    @api.depends('reservation_ids')
    def _compute_num_reservations(self):
        for rec in self:
            rec.num_reservations = len(rec.reservation_ids)

    @api.depends('reservation_ids.points')
    def _compute_loyalty_points(self):
        for customer in self:
            customer.loyalty_points = sum(customer.reservation_ids.mapped('points'))

    def update_loyalty_points(self):
        self.loyalty_points = sum(self.reservation_ids.mapped('points'))

    @api.depends('discount_percentage')
    def calculate_discount(self):
        for points in self:
            if points.loyalty_points < 100:
                points.discount_percentage = 0
            elif points.loyalty_points < 300:
                points.discount_percentage = 0.05
            elif points.loyalty_points < 500:
                points.discount_percentage = 0.1
            elif points.loyalty_points < 700:
                points.discount_percentage = 0.2
            elif points.loyalty_points < 900:
                points.discount_percentage = 0.3
            elif points.loyalty_points < 1100:
                points.discount_percentage = 0.4
            else:
                points.discount_percentage = 0.5








