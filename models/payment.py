from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools.safe_eval import datetime


class ProjektiPayment(models.Model):
    _name = 'projekti.payment'
    _description = 'Description'

    name = fields.Char()
    amount = fields.Float(string='Amount',  required=True, related='reservation_id.total_price')
    payment_date = fields.Date(string='Payment date', required=False, default=fields.Date.context_today)
    payment_status = fields.Selection(string='Payment status', required=False, default='pending',
                                      selection=[('pending', 'Pending'),
                                                 ('done', 'Done'),
                                                 ])
    payment_method = fields.Selection(string='Payment method', required=False,
                                      selection=[('cash', 'Cash'),
                                                 ('credit', 'Credit Card'),
                                                 ('bank transfer', 'Bank Transfer'),
                                                 ])
    reservation_id = fields.Many2one(comodel_name='projekti.reservations', string='Reservation', required=False,
                                     domain="[('customer_id', '=', customer_id),"
                                            "('state', '=', 'done')]"
                                     )
    customer_id = fields.Many2one(comodel_name='projekti.customer', string='Customer', required=False)
    payment_name = fields.Char(string='Payment Reference', compute='_compute_payment_name', store=True)
    #receipt_id = fields.Many2one(comodel_name='projekti.receipt', string='Receipt', required=False)

    @api.depends('reservation_id')
    def _compute_payment_name(self):
        for record in self:
            if record.reservation_id:
                name = 'Payment {} {}'.format(record.reservation_id.reservation_code,
                                              datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
                record.payment_name = name
            else:
                record.payment_name = False

    @api.onchange('customer_id')
    def _onchange_customer_id(self):
        if self.customer_id:
            reservations = self.env['projekti.reservations'].search([('customer_id', '=', self.customer_id.id),
                                                                     ('state', '=', 'done')])
            if reservations:
                self.reservation_id = reservations[0]
            else:
                self.reservation_id = False
        else:
            self.reservation_id = False


