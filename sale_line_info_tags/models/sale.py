# Copyright 2020 Jesus Ramiro <jesus@bilbonet.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models,  _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    info_tags_ids = fields.Many2many('sale.line.info.tags', string='Info Tags',)
