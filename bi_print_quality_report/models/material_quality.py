# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QualityOfMaterials(models.Model):
    _name = 'material.quality'

    # quality_check_id = fields.Many2one('quality.check')
    density = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="الكثافة و حجم الحبيبات")
    color = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="اللون")
    taste = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="الطعم")
    melting = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="الذوبان")
    matched_data = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="مطابقة البيانات على العبوات")
    exporting_doc = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="مستندات التوريد")