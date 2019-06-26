# -*- coding: utf-8 -*-

from odoo import models


class InheritQualityAlert(models.Model):
    _inherit = 'quality.alert'


    def print_quality_alert(self):
        return self.env.ref('bi_print_quality_alert_report.action_report_quality_alert').report_action(self)