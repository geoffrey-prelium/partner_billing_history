{
    'name': 'Partner Billing History',
    'version': '1.0',
    'category': 'Accounting/Accounting',
    'summary': 'Add N-1 billing field to partners',
    'description': """
        This module adds a computed field 'amount_invoiced_n_minus_1' to res.partner.
        It calculates the total invoiced amount (untaxed) for the previous calendar year.
    """,
    'depends': ['account'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
