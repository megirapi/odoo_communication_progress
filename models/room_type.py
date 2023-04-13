from odoo import fields, models, api


class ProjektiRoomType(models.Model):
    _name = 'projekti.room.type'
    _description = 'Description'

    name = fields.Char()
    no_bedrooms = fields.Integer(string='No_bedrooms', required=False)
    no_beds = fields.Integer( string='No_beds', required=False)
    floor = fields.Integer(string='Floor', required=False)
    view = fields.Selection(string='View', required=False,
                            selection=[('sea-view', 'Sea-View'),
                                       ('mountain-view', 'Mountain-View'),
                                       ('city-view', 'City-View'),
                                       ])


