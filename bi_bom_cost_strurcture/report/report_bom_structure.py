from odoo import api, models, _


class ReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'
    _description = 'BOM Structure Report'

    def _get_bom_lines(self, bom, bom_quantity, product, line_id, level):
        components, total = super(ReportBomStructure, self)._get_bom_lines(bom, bom_quantity, product, line_id, level)
        mrp_bom = self.env['mrp.bom.line']
        for component in components:
            line = mrp_bom.browse(component['line_id'])
            if line:
                component['available_qty'] = line.available_qty
        return components, total

    def _get_pdf_line(self, bom_id, product_id=False, qty=1, child_bom_ids=[], unfolded=False):
        data = super(ReportBomStructure, self)._get_pdf_line(bom_id, product_id, qty, child_bom_ids, unfolded)
        bom = self.env['mrp.bom'].browse(bom_id)
        all_data = self._get_bom(bom_id=bom_id, product_id=product_id or bom.product_id or bom.product_tmpl_id.product_variant_id, line_qty=qty)
        for pdf_line in data['lines']:
            pdf_line['available_qty'] = 0.0
            for component_line in all_data['components']:
                if pdf_line['name'] == component_line['prod_name']:
                    pdf_line['available_qty'] = component_line['available_qty']
        return data
