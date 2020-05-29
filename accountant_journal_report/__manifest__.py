# Copyright 2019 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Accountant Journal Report',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Journal ledger for your accountant advisor',
    'license': 'AGPL-3',
    'author': 'Jesus Ramiro (Bilbonet.NET)',
    'website': 'https://www.bilbonet.net',
    'depends': [
        'account_financial_report',
    ],
    'data': [
        'wizard/accountant_journal_ledger_wizard_view.xml',
        'report/templates/layouts.xml',
        'report/accountant_journal_ledger.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
