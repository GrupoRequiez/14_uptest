# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Rubén Bravo <rubenred18@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = 'account.move'

    brand = fields.Char('Brand',
                        compute='_compute_brand_id',
                        search='_search_brand',
                        readonly=True)

    def _compute_brand_id(self):
        for move in self:
            if move.invoice_line_ids and move.move_type not in ('entry', 'out_receipt', 'in_receipt'):
                if move.invoice_line_ids[0].product_id.product_brand_id:
                    move.brand = self.invoice_line_ids[0].product_id.product_brand_id.name
        return move.brand

    def _search_brand(self, operator, value):
        AccountMove = self.env['account.move']
        invoices = AccountMove.search([])
        list_ids = []
        for invoice in invoices:
            if invoice.invoice_line_ids:
                if invoice.invoice_line_ids[0].product_id.product_brand_id:
                    brand = invoice.invoice_line_ids[0].product_id.product_brand_id.name
                    if operator == '=':
                        if brand == value:
                            list_ids.append(invoice.id)
                    elif operator == '!=':
                        if brand != value:
                            list_ids.append(invoice.id)
        return [('id', 'in', list_ids)]
