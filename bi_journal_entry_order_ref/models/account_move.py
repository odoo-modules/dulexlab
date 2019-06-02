# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    ref_order = fields.Char('Order Ref')

    @api.model
    def create(self, vals):
        res = super(AccountMoveLine, self).create(vals)
        ref_order = False
        if res.invoice_id.origin:
            ref_order = res.invoice_id.origin

        elif res.move_id.stock_move_id.picking_id.group_id:
            ref_order = res.move_id.stock_move_id.picking_id.group_id.name
        res.update({
            'ref_order': ref_order,
        })
        return res

    @api.model
    def set_ref_order(self):
        lines = self.env['account.move.line'].search([('account_id.code', 'ilike', '210400')])
        for line in lines:
            ref_order = False
            if line.invoice_id and line.invoice_id.origin:
                ref_order = line.invoice_id.origin
            elif line.move_id.stock_move_id.picking_id.group_id:
                ref_order = line.move_id.stock_move_id.picking_id.group_id.name
            line.update({
                'ref_order': ref_order,
            })

    # @api.multi
    # @api.depends('invoice_id', 'invoice_id.origin', 'move_id', 'move_id.stock_move_id',
    #              'move_id.stock_move_id.picking_id.group_id')
    # def _get_ref_order(self):
    #     for line in self:
    #         ref_order = False
    #         if line.invoice_id.origin:
    #             ref_order = line.invoice_id.origin
    #
    #         elif line.move_id.stock_move_id.picking_id.group_id:
    #             ref_order = line.move_id.stock_move_id.picking_id.group_id
    #
    #         line.update({
    #             'ref_order': ref_order,
    #         })
