# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from lxml import etree
from odoo.osv.orm import setup_modifiers


class ProductProduct(models.Model):
    _inherit = 'product.product'

    batch_sequence = fields.Integer(string="Batch Number", related="product_tmpl_id.batch_sequence")
    batch_step = fields.Integer(string="Batch Step", related="product_tmpl_id.batch_step")
    batch_month = fields.Integer(string="Batch Change Date", related="product_tmpl_id.batch_month")

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ProductProduct, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='batch_sequence']"):
                node.set('readonly', '1')
                setup_modifiers(node, res['fields']['batch_sequence'])
            for node in doc.xpath("//field[@name='batch_step']"):
                node.set('readonly', '1')
                setup_modifiers(node, res['fields']['batch_step'])
            res['arch'] = etree.tostring(doc)
        return res
