# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval
from odoo.tools import pycompat


class AccountantJournalLedgerReportWizard(models.TransientModel):
    """Accountant Journal Ledger report wizard."""

    _name = 'accountant.journal.ledger.report.wizard'
    _description = "Journal Ledger Report Wizard"

    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.user.company_id,
        string='Company',
        required=False,
        ondelete='cascade',
    )
    date_range_id = fields.Many2one(
        comodel_name='date.range',
        string='Date range',
    )
    date_from = fields.Date(
        string="Start date",
        required=True
    )
    date_to = fields.Date(
        string="End date",
        required=True
    )
    journal_id = fields.Many2one(
        comodel_name='account.journal',
        string="Journals",
        required=False,
    )
    move_target = fields.Selection(
        selection='_get_move_targets',
        default='all',
        required=True,
    )
    sort_option = fields.Selection(
        selection='_get_sort_options',
        string="Sort entries by",
        default='name',
        required=True,
    )
    with_account_name = fields.Boolean(
        default=False,
    )

    @api.model
    def _get_move_targets(self):
        return [
            ('all', _("All")),
            ('posted', _("Posted")),
            ('draft', _("Not Posted"))
        ]

    @api.model
    def _get_sort_options(self):
        return [
            ('name', _("Entry number")),
            ('date', _("Date")),
        ]


    @api.onchange('date_range_id')
    def onchange_date_range_id(self):
        self.date_from = self.date_range_id.date_start
        self.date_to = self.date_range_id.date_end

    @api.onchange('company_id')
    def onchange_company_id(self):
        """Handle company change."""
        if self.company_id and self.date_range_id.company_id and \
                self.date_range_id.company_id != self.company_id:
            self.date_range_id = False
        if self.company_id and self.journal_id:
            self.journal_id = self.journal_id.filtered(
                lambda p: p.company_id == self.company_id or not p.company_id)
        res = {'domain': {'journal_id': []}}
        if not self.company_id:
            return res
        else:
            res['domain']['journal_id'] += [
                ('company_id', '=', self.company_id.id)]
        return res

    @api.multi
    def button_export_html(self):
        # self.ensure_one()
        # action = self.env.ref(
        #     'accountant_journal_report.action_report_accountant_journal_ledger')
        # vals = action.read()[0]
        # context1 = vals.get('context', {})
        # if isinstance(context1, pycompat.string_types):
        #     context1 = safe_eval(context1)
        # model = self.env['report_accountant_journal_ledger']
        # report = model.create(self._prepare_report_journal_ledger())
        # #report.compute_data_for_report()
        # context1['active_id'] = report.id
        # context1['active_ids'] = report.ids
        # vals['context'] = context1
        # return vals
        data = self._prepare_report_journal_ledger()
        # data['form'] = self.read(['date_from','date_to'])
        return self.env.ref(
            'accountant_journal_report.action_report_accountant_journal_ledger_html'
        ).report_action(self, data=data)

    @api.multi
    def button_export_pdf(self):
        data = self._prepare_report_journal_ledger()
        return self.env.ref(
            'accountant_journal_report.action_report_accountant_journal_ledger_qweb'
        ).report_action(self, data=data)

    @api.multi
    def _prepare_report_journal_ledger(self):
        self.ensure_one()
        return {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'move_target': self.move_target,
            'company_id': self.company_id.id,
            'journal_id': self.journal_id.id,
            'sort_option': self.sort_option,
            'with_account_name': self.with_account_name,
        }

