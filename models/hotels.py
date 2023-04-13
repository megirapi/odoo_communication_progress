from odoo import fields, models, api


class ProjektiHotels(models.Model):
    _name = 'projekti.hotels'
    _description = 'Description'

    name = fields.Char(string="Hotel Name", requried=True)
    address = fields.Char(string='Adress', required=True)
    country = fields.Char(string='Country', required=False)
    city = fields.Char(string='City', required=False)
    no_rooms = fields.Integer(string='No_rooms', required=False)
    tel = fields.Char(string='Tel', required=False)
    website = fields.Char(string='Webisite', required=False)

    room_ids = fields.One2many(comodel_name='projekti.rooms', inverse_name='hotel_id', string='Rooms', required=False)
