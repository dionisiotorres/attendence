# Copyright <2020> bilbonet.net - Jesus Ramiro
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api

DIGITS = (16, 2)


class ReportAccountantJournalLedger(models.AbstractModel):
    _name = 'report.accountant_journal_report.accountant_journal_report'
    _description = 'Accountant Journal Ledger Report'


    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        domain = [
            ('date', '>=', data['date_from']),
            ('date', '<=', data['date_to']),
            ('journal_id', '=', data['journal_id'])
        ]
        if data['move_target'] != 'all':
            domain += [('state', '=', data['move_target'])]

        moves = self.env['account.move'].search(
            domain, order=data['sort_option']
        )

        total_debit_credit = self.get_total_debit_credit(moves)

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
            'moves': moves,
            'totals': total_debit_credit,
        }
        return docargs

    def get_total_debit_credit(self, moves):
        # sum_move_debit = 0
        # sum_move_credit = 0
        res= {}
        sum_tot_debit = 0
        sum_tot_credit = 0
        for move in moves:
            sum_move_debit = sum(move.line_ids.mapped('debit'))
            sum_move_credit = sum(move.line_ids.mapped('credit'))
            res.update({move.id:
                {'sum_move_debit': sum_move_debit,
                'sum_move_credit': sum_move_credit}
                })
            sum_tot_debit += sum(move.line_ids.mapped('debit'))
            sum_tot_credit += sum(move.line_ids.mapped('credit'))

        res.update({
            'sum_tot_debit': sum_tot_debit,
            'sum_tot_credit': sum_tot_credit
        })
        return res
        # return(
        #     {'sum_tot_debit': sum_tot_debit,
        #     'sum_tot_credit': sum_tot_credit})


