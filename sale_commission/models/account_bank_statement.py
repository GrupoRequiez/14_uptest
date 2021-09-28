from odoo import api, fields, models, _


class AccountBankStatementLine(models.Model):
    _name = "account.bank.statement.line"
    _inherit = "account.bank.statement.line"

    def button_undo_reconciliation(self):
        for line in self.line_ids:
            reconcile_line_id = self.env['account.move.line'].search(
                [('id', 'in', line.move_id.line_ids._reconciled_lines()), ('move_id.move_type', '=', 'out_invoice')], limit=1)
            payment_line_id = self.env['account.move.line'].search(
                [('id', 'in', line.move_id.line_ids._reconciled_lines()), ('move_id.move_type', '!=', 'out_invoice')], limit=1)
            assoc = self.env['account.association'].search([
                ('move_line_id', '=', reconcile_line_id.id),
                ('payment_amount', '=', payment_line_id.credit)], limit=1)
            assoc.unlink()
            break
        return super(AccountBankStatementLine, self).button_undo_reconciliation()
