# Copyright 2018 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Order Lines Information Tags',
    'version': '12.0.1.0.0',
    'category': 'Sales',
    'summary': 'Sale Order Lines Information Tags',
    'description': """
This module allow you define information tags and select them in sale order lines.
    """,
    'license': 'AGPL-3',
    'author': 'Jesus Ramiro (Bilbonet.NET)',
    'website': 'https://www.bilbonet.net',
    'depends': ['sale',],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_line_info_tags.xml',
        'views/sale_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
