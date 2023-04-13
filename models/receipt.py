from lxml import etree
from odoo import fields, models, api
from odoo.exceptions import UserError


class ProjektiReceipt(models.Model):
    _name = 'projekti.receipt'
    _description = 'Description'

    receipt_no = fields.Integer(string='Receipt number', required=False)
    date = fields.Datetime(string='Date', required=True)
    amount = fields.Float(string='Amount', required=False, compute='_compute_total')
    state = fields.Selection(string='State', required=True, default='draft',
                             selection=[('draft', 'Draft'),
                                        ('done', 'Confirmed'),
                                        ('cancel', 'Cancelled'),
                                        ])
    customer_id = fields.Many2one(comodel_name='projekti.customer', string='Customer', required=True)
    receipt_lines_ids = fields.One2many(comodel_name='projekti.receipt.lines', inverse_name='receipt_id',
                                        string='Receipt Lines', required=False)

    @api.depends('receipt_lines_ids')
    def _compute_total(self):
        for rec in self:
            rec.amount = sum(rec.receipt_lines_ids.mapped('amount'))

    def aprove(self):
        self.state = "done"

    def anullo(self):
        self.state = "cancel"

    def draft(self):
        self.state = "draft"

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError("You can't delete the invoice!")
        return super(ProjektiReceipt, self).unlink()

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ProjektiReceipt, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                           submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for field in doc.xpath("//field[@name='reservation_id']"):
                domain = [('customer_id', '=', self.customer_id.id)]
                field.set('domain', str(domain))
            res['arch'] = etree.tostring(doc)
        return res


class ProjektiReceiptLines(models.Model):
    _name = 'projekti.receipt.lines'
    _description = 'ProjektiReceiptLines'

    reservation_id = fields.Many2one(comodel_name='projekti.reservations', string='Reservation', required=False,
                                     domain="[('customer_id','=',parent.customer_id)]")
    receipt_id = fields.Many2one(comodel_name='projekti.receipt', string='Receipt', required=False)
    amount = fields.Float(string='Amount', required=False, related='reservation_id.total_price')
    date = fields.Datetime(related='receipt_id.date', string='Date', required=False)

    @api.onchange('receipt_id.customer_id')
    def onchange_customer_id(self):
        domain = [('id', '=', -1)]  # default domain to return no results
        if self.receipt_id.customer_id:
            domain = [('customer_id', '=', self.receipt_id.customer_id.id)]
        return {'domain': {'reservation_id': domain}}









