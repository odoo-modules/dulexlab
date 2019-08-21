# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QualityCheckReport(models.Model):
    _inherit = 'quality.check'

    def print_quality_check(self):
        return self.env.ref('bi_print_quality_report.action_report_quality_check').report_action(self)

    # materials_id = fields.One2many('material.quality', 'quality_check_id', string="materials_id")
    current_date = fields.Date(string="Date")

    density = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="الكثافة وحجم الحبيبات")
    color = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="اللون")
    taste = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="الطعم")
    melting = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="الذوبان")
    matched_data = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="مطابقة البيانات على العبوات")
    exporting_doc = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="مستندات التوريد")
    density_note = fields.Char(string='ملاحظات')
    color_note = fields.Char(string='ملاحظات')
    taste_note = fields.Char(string='ملاحظات')
    melting_note = fields.Char(string='ملاحظات')
    matched_note = fields.Char(string='ملاحظات')
    exporting_note = fields.Char(string='ملاحظات')

    work_on_machines = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="التشغيل على الماكينات")
    thickness = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="السمك")
    glue_qual = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="جودة اللحام")
    printing_qual = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="جودة الطباعة")
    matching_data = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="مطابقة البيانات")
    exporting_documents = fields.Selection([('ch1', 'مقبول'), ('ch2', 'غير مقبول')], string="مستندات التوريد")
    work_on_machines_note = fields.Char(string='ملاحظات')
    thickness_note = fields.Char(string='ملاحظات')
    glue_qual_note = fields.Char(string='ملاحظات')
    printing_qual_note = fields.Char(string='ملاحظات')
    matching_data_note = fields.Char(string='ملاحظات')
    exporting_documents_note = fields.Char(string='ملاحظات')
    accepted = fields.Boolean(string="مقبول")
    not_accepted = fields.Boolean(string="غير مقبول")