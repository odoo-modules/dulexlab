from odoo import models, fields, api, _
from odoo.tools.misc import formatLang


class AccountFinancialReportLine(models.Model):
    _inherit = "account.financial.html.report.line"

    calculation_mab = {
        'net_sales': 0.0,
        # 'total_expenses': 0.0,
        # 'total_interest': 0.0,
        # 'total_general_tax': 0.0,
        # 'total_other_income': 0.0,
    }
    @api.multi
    def _get_lines(self, financial_report, currency_table, options, linesDicts):
        res = super(AccountFinancialReportLine, self)._get_lines(financial_report, currency_table, options, linesDicts)
        if financial_report.name in ['Income Statement', 'الأرباح و الخسائر']:
            for line in res:
                for i, col in enumerate(line['columns']):
                    if i > 0:
                        break
                    field_name = ''
                    if 'no_format_name' in col:
                        field_name = 'no_format_name'
                    elif 'name' in col and col['name'] and (type(col['name']) == float):
                        field_name = 'name'
                    if field_name:
                        if line['name'] == 'Sales':
                            self.calculation_mab['net_sales'] = float(col[field_name])
                        # elif line['name'] in ['الإجمالي Expenses', 'Total Expenses']:
                        #     self.calculation_mab['total_expenses'] = float(col[field_name])
                        # elif line['name'] in ['الإجمالي Interest', 'Total Interest']:
                        #     self.calculation_mab['total_interest'] = float(col[field_name])
                        # elif line['name'] in ['الإجمالي General Tax', 'Total General Tax']:
                        #     self.calculation_mab['total_general_tax'] = float(col[field_name])
                        # elif line['name'] in ['الإجمالي Other Income', 'Total Other Income']:
                        #     self.calculation_mab['total_other_income'] = float(col[field_name])

            for line in res:
                for i, col in enumerate(line['columns']):
                    line_name = ''
                    if line['name'] in [
                        'الدخل التشغيلي', 'Net Sales', 'تكاليف الدخل', 'Cost of Goods Sold (COGS)',
                        'الإجمالي إجمالي الربح', 'Total Gross Profit', 'الإجمالي الدخل', 'Total Income',
                        'الإجمالي المصروفات', 'Total Expenses and Depreciation', 'صافي الربح',
                        'Net Profit Before Interest', 'الإجمالي Interest', 'Total Interest',
                        'Net Profit Before Tax', 'الإجمالي General Tax', 'Total General Tax',
                        'الإجمالي Other Income', 'Total Other Income', 'Net Profit after Tax'
                    ] or line['name'] in [
                        'Salaries Expense', 'Admin Salaries Expenses', 'Admin Expenses',
                        'Distribution Expenses', 'Hr Expenses', 'Regestration Expenses', 'Marketing Expenses',
                        'Other Marketing Expenses', 'Factory expenses', 'الإجمالي Expenses', 'Total Expenses',
                        'إستهلاك', 'Depreciation'
                    ] or line['name'] in [
                        'Bank Interest', 'Capital Interest'
                    ] or line['name'] in [
                        'TAX'
                    ] or line['name'] in [
                        'Other Income'
                    ] or line['name'] in [
                        'Sales', 'Discount', 'Gain & Loss from other investment'
                    ]:
                        line_name = 'net_sales'
                    # elif line['name'] in [
                    #     'Salaries Expense', 'Admin Salaries Expenses', 'Admin Expenses',
                    #     'Distribution Expenses', 'Hr Expenses', 'Regestration Expenses', 'Marketing Expenses',
                    #     'Other Marketing Expenses', 'Factory expenses', 'الإجمالي Expenses', 'Total Expenses',
                    #     'إستهلاك', 'Depreciation'
                    # ]:
                    #     line_name = 'total_expenses'
                    # elif line['name'] in ['Bank Interest', 'Capital Interest']:
                    #     line_name = 'total_interest'
                    # elif line['name'] in ['TAX']:
                    #     line_name = 'total_general_tax'
                    # elif line['name'] in ['Other Income']:
                    #     line_name = 'total_other_income'

                    if line_name:
                        if 'no_format_name' in col:
                            if self.calculation_mab[line_name] == 0.0:
                                col['percent'] = '  0.00 %'
                            else:
                                col['percent'] = '  ' + '{0:,.2f}'.format(100 * (float(col['no_format_name']) / self.calculation_mab[line_name])) + ' % '
                        elif self._context.get('print_mode') and self._context.get('no_format') and not self._context.get('prefetch_fields') and (col['name'] or col['name'] == 0.0):
                            if type(col['name']) is float:
                                if self.calculation_mab[line_name] == 0.0:
                                    col['col_name'] = '0.00%'
                                else:
                                    col['col_name'] = '{0:,.2f}'.format(100 * (float(col['name']) / self.calculation_mab[line_name])) + '%'
        return res
