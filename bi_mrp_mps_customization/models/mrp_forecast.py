from odoo import api, fields, models


class SaleForecast(models.Model):
    _inherit = 'sale.forecast'

    @api.model
    def save_forecast_data(self, product_id=False, quantity=0, date=False, date_to=False, field=None, period=False):
        print(product_id, quantity, date, date_to, field, period)
        product = self.env['product.product'].browse(product_id)
        bom = self.env['mrp.bom']._bom_find(product=product)
        if bom:
            product.apply_active = True
        domain = [('product_id', '=', product_id), ('date', '>=', str(date)), ('date', '<', str(date_to))]
        if field == 'forecast_qty':
            domain += [('mode', '=', 'auto')]
        else:
            domain += [('mode', '=', 'manual')]
        forecasts = self.search(domain, order="date")
        print("XXx")
        if field == 'forecast_qty':
            qty_period = sum(forecasts.mapped('forecast_qty'))
            new_quantity = quantity - qty_period
            if forecasts:
                forecasts[0].write({'forecast_qty': forecasts[0].forecast_qty + new_quantity})
            else:
                self.create({'date': date, 'product_id': product_id, 'forecast_qty': new_quantity})
        if field == 'to_supply':
            if quantity is False:
                # If you put it back to manual, then delete the to_supply
                forecasts.filtered(lambda x: x.state != 'done').unlink()
            else:
                qty_supply = sum(forecasts.mapped('to_supply'))
                new_quantity = quantity - qty_supply
                if forecasts and forecasts[0].date == fields.Date.from_string(date):
                    forecasts[0].write({'to_supply': forecasts[0].to_supply + new_quantity})
                else:
                    self.create({'date': date, 'product_id': product_id, 'to_supply': new_quantity, 'mode': 'manual'})
