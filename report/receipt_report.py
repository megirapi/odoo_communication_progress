from odoo import fields, models, api


class ProjektiReportReceipt(models.AbstractModel):
    _name = 'report.projekti.report_receipt'
    _description = 'Receipt Invoice'

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = [('date', '>=', data['start_date']), ('date', '<', data['end_date'])]

        if not data['res_ids']:
            name = 'All reservations'
        else:
            domain.append(('reservation_id', 'in', data['res_ids']))
            reservations = self.env['projekti.receipt.lines'].browse(data['res_ids']).mapped("reservation_id")
            name = f'reservations {", ".join(map(str, reservations))}'

        receipt_lines_obj = self.env['projekti.receipt.lines'].search(domain)
        receipt_lines = []

        for rec in receipt_lines_obj:
            receipt_lines.append({
                'reservations': rec.reservation_id.reservation_code,
                'amount': rec.amount,
                'date': rec.date,
            })
        return {
            'docs': receipt_lines,
            'r_name': name,
        }



