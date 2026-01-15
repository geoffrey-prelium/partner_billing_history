from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class ResPartner(models.Model):
    _inherit = 'res.partner'

    amount_invoiced_n_minus_1 = fields.Monetary(
        string="Billed Amount N-1",
        compute='_compute_amount_invoiced_n_minus_1',
        currency_field='company_currency_id',
        help="Total untaxed billed amount for the previous year."
    )
    company_currency_id = fields.Many2one(
        'res.currency', 
        string='Company Currency', 
        related='company_id.currency_id', 
        readonly=True
    )

    @api.depends('invoice_ids.state', 'invoice_ids.invoice_date', 'invoice_ids.move_type')
    def _compute_amount_invoiced_n_minus_1(self):
        today = fields.Date.context_today(self)
        prev_year = today.year - 1
        start_date = f'{prev_year}-01-01'
        end_date = f'{prev_year}-12-31'

        # Fetch data grouped by partner
        domain = [
            ('partner_id', 'in', self.ids),
            ('move_type', 'in', ('out_invoice', 'out_refund')),
            ('state', '=', 'posted'),
            ('invoice_date', '>=', start_date),
            ('invoice_date', '<=', end_date),
        ]
        
        # We use read_group for performance optimization
        group_data = self.env['account.move'].read_group(
            domain,
            ['partner_id', 'amount_untaxed_signed'],
            ['partner_id']
        )
        
        data_map = {item['partner_id'][0]: item['amount_untaxed_signed'] for item in group_data}

        for partner in self:
            partner.amount_invoiced_n_minus_1 = data_map.get(partner.id, 0.0)
