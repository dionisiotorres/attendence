# Copyright 2020 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models,  _


class SaleLineInfoTags(models.Model):
    _name = "sale.line.info.tags"
    _description = "Tags in sale order line"

    name = fields.Char(required=True)
    color = fields.Integer(string='Color Index', default=10)

    _sql_constraints = [
        ('sale_line_info_tag_name_uniq', 'unique (name)',
         _('Tag name already exists !')),
    ]