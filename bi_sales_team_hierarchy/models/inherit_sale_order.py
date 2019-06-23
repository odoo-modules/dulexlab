# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.odoo.exceptions import UserError


class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'

    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', required=True,
                              default="")
    team_id = fields.Many2one('crm.team', related='user_id.sale_team_id')
    area = fields.Many2one('new.area', string="Area", related='user_id.area', readonly=False)
    team_supervisor = fields.Many2one('res.users', related='team_id.team_supervisor', srting="Team Supervisor")
    team_leader = fields.Many2one('res.users', related='team_id.user_id', srting="Team Leader")
    # vehicle_id = fields.Many2one('fleet.vehicle')
    driver_name = fields.Many2one('res.partner', related='car_number.driver_id', readonly=False, string="Driver Name",
                                  required=True)
    car_number = fields.Many2one('fleet.vehicle', string="Car Number")

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(InheritSaleOrder, self)._prepare_invoice()
        invoice_vals['area'] = self.area.id or False
        invoice_vals['team_supervisor'] = self.team_supervisor.id or False
        invoice_vals['team_leader'] = self.team_leader.id or False
        invoice_vals['driver_name'] = self.driver_name.id or False
        invoice_vals['car_number'] = self.car_number.id or False
        return invoice_vals


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    _description = "Sales Advance Payment Invoice"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        inv_obj = self.env['account.invoice']
        ir_property_obj = self.env['ir.property']

        account_id = False
        if self.product_id.id:
            account_id = self.product_id.property_account_income_id.id or self.product_id.categ_id.property_account_income_categ_id.id
        if not account_id:
            inc_acc = ir_property_obj.get('property_account_income_categ_id', 'product.category')
            account_id = order.fiscal_position_id.map_account(inc_acc).id if inc_acc else False
        if not account_id:
            raise UserError(
                _(
                    'There is no income account defined for this product: "%s". You may have to install a chart of account from Accounting app, settings menu.') %
                (self.product_id.name,))

        if self.amount <= 0.00:
            raise UserError(_('The value of the down payment amount must be positive.'))
        context = {'lang': order.partner_id.lang}
        if self.advance_payment_method == 'percentage':
            amount = order.amount_untaxed * self.amount / 100
            name = _("Down payment of %s%%") % (self.amount,)
        else:
            amount = self.amount
            name = _('Down Payment')
        del context
        taxes = self.product_id.taxes_id.filtered(lambda r: not order.company_id or r.company_id == order.company_id)
        if order.fiscal_position_id and taxes:
            tax_ids = order.fiscal_position_id.map_tax(taxes, self.product_id, order.partner_shipping_id).ids
        else:
            tax_ids = taxes.ids

        invoice = inv_obj.create({
            'name': order.client_order_ref or order.name,
            'origin': order.name,
            'type': 'out_invoice',
            'reference': False,
            'account_id': order.partner_id.property_account_receivable_id.id,
            'partner_id': order.partner_invoice_id.id,
            'partner_shipping_id': order.partner_shipping_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': name,
                'origin': order.name,
                'account_id': account_id,
                'price_unit': amount,
                'quantity': 1.0,
                'discount': 0.0,
                'uom_id': self.product_id.uom_id.id,
                'product_id': self.product_id.id,
                'sale_line_ids': [(6, 0, [so_line.id])],
                'invoice_line_tax_ids': [(6, 0, tax_ids)],
                'analytic_tag_ids': [(6, 0, so_line.analytic_tag_ids.ids)],
                'account_analytic_id': order.analytic_account_id.id or False,
            })],
            'currency_id': order.pricelist_id.currency_id.id,
            'payment_term_id': order.payment_term_id.id,
            'fiscal_position_id': order.fiscal_position_id.id or order.partner_id.property_account_position_id.id,
            'team_id': order.team_id.id,
            'user_id': order.user_id.id,
            'comment': order.note,
            'area': order.area.id or False,
            'team_supervisor' : order.team_supervisor.id or False,
            'team_leader' : order.team_leader.id or False,
            'driver_name' : order.driver_name.id or False,
            'car_number' : order.car_number.id or False,
        })
        invoice.compute_taxes()
        invoice.message_post_with_view('mail.message_origin_link',
                                       values={'self': invoice, 'origin': order},
                                       subtype_id=self.env.ref('mail.mt_note').id)
        return invoice
