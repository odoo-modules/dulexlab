# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class MrpWorkcenterProductivity(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    pause_reason_id = fields.Many2one(
        'work.order.pause.reason', string="Pause Reason", readonly=True, ondelete="restrict")


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    pause_reason_id = fields.Many2one(
        'work.order.pause.reason', string="Pause Reason", readonly=True, ondelete="restrict")

    @api.multi
    def end_previous(self, doall=False):
        """
        @param: doall:  This will close all open time lines on the open work orders when doall = True, otherwise
        only the one of the current user
        """
        # TDE CLEANME
        timeline_obj = self.env['mrp.workcenter.productivity']
        domain = [('workorder_id', 'in', self.ids), ('date_end', '=', False)]
        if not doall:
            domain.append(('user_id', '=', self.env.user.id))
        not_productive_timelines = timeline_obj.browse()
        for timeline in timeline_obj.search(domain, limit=None if doall else 1):
            wo = timeline.workorder_id
            if wo.duration_expected <= wo.duration:
                if timeline.loss_type == 'productive':
                    not_productive_timelines += timeline
                timeline.write({'date_end': fields.Datetime.now()})
            else:
                maxdate = fields.Datetime.from_string(timeline.date_start) + relativedelta(
                    minutes=wo.duration_expected - wo.duration)
                enddate = datetime.now()
                if maxdate > enddate:
                    timeline.write({'date_end': enddate})
                else:
                    timeline.write({'date_end': maxdate})
                    not_productive_timelines += timeline.copy({'date_start': maxdate, 'date_end': enddate})
            if self._context.get('order_paused'):
                timeline.write({'pause_reason_id': timeline.workorder_id.pause_reason_id.id})

        if not_productive_timelines:
            loss_id = self.env['mrp.workcenter.productivity.loss'].search([('loss_type', '=', 'performance')], limit=1)
            if not len(loss_id):
                raise UserError(_(
                    "You need to define at least one unactive productivity loss in the category 'Performance'. Create one from the Manufacturing app, menu: Configuration / Productivity Losses."))
            not_productive_timelines.write({'loss_id': loss_id.id})

        return True
