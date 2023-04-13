from odoo import fields, models, api


class ReceiptReport(models.TransientModel):
    _name = 'receipt.report'
    _description = 'Receipt report'

    res_ids = fields.Many2many(comodel_name='projekti.reservations', string='Reservations')
    start_date = fields.Date(default=fields.Datetime.now, string='Start date', required=True)
    end_date = fields.Date(default=fields.Datetime.now, string='End date', required=True)

    def print_report(self):
        self.ensure_one()
        data = {
            "res_ids": self.res_ids.ids,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }

        return self.env.ref('projekti.action_report_receipt').report_action(None, data=data)