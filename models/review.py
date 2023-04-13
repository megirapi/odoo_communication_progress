from odoo import fields, models, api


class ProjektiReview(models.Model):
    _name = 'projekti.review'
    _description = 'Customer Reviews'

    customer_id = fields.Many2one('projekti.customer', string='Customer')
    employee_id = fields.Many2one('projekti.employees', string='Employee')
    date = fields.Date(string='Date', default=fields.Date.today(), required=True)
    hotel_id = fields.Many2one('projekti.hotels', string='Hotel', required=True)
    review = fields.Text(string='Review')
    rating = fields.Selection(string='Hotel Star Rating', required=True,
                              selection=[('0', 'Very low'),
                                         ('1', 'Low'),
                                         ('2', 'Normal'),
                                         ('3', 'High'),
                                         ('4', 'Very High'),
                                         ('4', 'Excellent')
                                         ])
    feedback = fields.Text(string='Feedback',  required=True)



