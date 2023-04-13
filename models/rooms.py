from odoo import fields, models, api


class ProjektiRooms(models.Model):
    _name = 'projekti.rooms'
    _description = 'Description'

    room_no = fields.Integer(string='Room number', required=False)
    price = fields.Integer(string='Price',  required=True)
    status = fields.Selection(string='Status', required=True,
                              selection=[('occupied', 'Occupied'),
                                         ('ready', 'Ready'),
                                         ('maintenance', 'Maintenance'),
                                         ])
    capacity = fields.Integer(string='Capacity', required=True)
    type_id = fields.Many2one(comodel_name='projekti.room.type', string='Room Type', required=False)
    #reservation_id = fields.Many2one(comodel_name='projekti.reservations', string='Reservation_id', required=False)
    hotel_id = fields.Many2one(comodel_name='projekti.hotels', string='Hotel', required=False)

