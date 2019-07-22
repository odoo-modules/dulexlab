from odoo import api, fields, models
from math import ceil
from datetime import datetime, timedelta
import calendar


class SaleForecast(models.Model):
    _inherit = 'sale.forecast'

    @api.model
    def save_forecast_data(self, product_id=False, quantity=0, date=False, date_to=False, field=None, period=False):
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
        if field == 'forecast_qty':
            if period == 'day':
                qty_period = sum(forecasts.mapped('forecast_qty'))
                new_quantity = quantity - qty_period
                if forecasts:
                    forecasts[0].write({'forecast_qty': forecasts[0].forecast_qty + new_quantity})
                else:
                    self.create({'date': date, 'product_id': product_id, 'forecast_qty': new_quantity})
            elif period == 'week':
                new_quantity = quantity
                new_quantity_per_day = new_quantity / 6
                new_quantity_per_day = ceil(new_quantity_per_day)
                start_date = datetime.strptime(date, '%Y-%m-%d')
                for i in range(0, 7, 1):
                    new_date = start_date + timedelta(days=i)
                    if calendar.day_name[new_date.weekday()] != 'Friday':
                        forecast = self.search(
                            [('product_id', '=', product_id), ('date', '=', str(new_date.date())),
                             ('mode', '=', 'auto')])
                        qty = (new_quantity_per_day if new_quantity >= new_quantity_per_day else (
                            new_quantity if new_quantity > 0 else 0))
                        if forecast:
                            forecast.forecast_qty = qty
                        else:
                            self.create({'date': str(new_date.date()), 'product_id': product_id, 'forecast_qty': qty,
                                         'mode': 'auto'})
                        new_quantity -= new_quantity_per_day
            elif period == 'month':
                new_quantity = quantity
                new_quantity_per_day = new_quantity / 24
                new_quantity_per_day = ceil(new_quantity_per_day)
                start_date = datetime.strptime(date, '%Y-%m-%d')
                for i in range(0, 28, 1):
                    new_date = start_date + timedelta(days=i)
                    if calendar.day_name[new_date.weekday()] != 'Friday':
                        forecast = self.search(
                            [('product_id', '=', product_id), ('date', '=', str(new_date.date())),
                             ('mode', '=', 'auto')])
                        qty = (new_quantity_per_day if new_quantity >= new_quantity_per_day else (
                            new_quantity if new_quantity > 0 else 0))
                        if forecast:
                            forecast.forecast_qty = qty
                        else:
                            self.create({'date': str(new_date.date()), 'product_id': product_id, 'forecast_qty': qty,
                                         'mode': 'auto'})
                        new_quantity -= new_quantity_per_day
        if field == 'to_supply':
            if quantity is False:
                # If you put it back to manual, then delete the to_supply
                forecasts.filtered(lambda x: x.state != 'done').unlink()
            else:
                if period == 'day':
                    qty_supply = sum(forecasts.mapped('to_supply'))
                    new_quantity = quantity - qty_supply
                    if forecasts and forecasts[0].date == fields.Date.from_string(date):
                        forecasts[0].write({'to_supply': forecasts[0].to_supply + new_quantity})
                    else:
                        self.create(
                            {'date': date, 'product_id': product_id, 'to_supply': new_quantity, 'mode': 'manual'})
                elif period == 'week':
                    new_quantity = quantity
                    new_quantity_per_day = new_quantity / 6
                    new_quantity_per_day = ceil(new_quantity_per_day)
                    start_date = datetime.strptime(date, '%Y-%m-%d')
                    for i in range(0, 7, 1):
                        new_date = start_date + timedelta(days=i)
                        if calendar.day_name[new_date.weekday()] != 'Friday':
                            forecast = self.search(
                                [('product_id', '=', product_id), ('date', '=', str(new_date.date())),
                                 ('mode', '=', 'manual')])
                            qty = (new_quantity_per_day if new_quantity >= new_quantity_per_day else (
                                new_quantity if new_quantity > 0 else 0))
                            if forecast:
                                forecast.to_supply = qty
                            else:
                                self.create(
                                    {'date': str(new_date.date()), 'product_id': product_id, 'to_supply': qty,
                                     'mode': 'manual'})
                            new_quantity -= new_quantity_per_day
                elif period == 'month':
                    new_quantity = quantity
                    new_quantity_per_day = new_quantity / 24
                    new_quantity_per_day = ceil(new_quantity_per_day)
                    start_date = datetime.strptime(date, '%Y-%m-%d')
                    for i in range(0, 28, 1):
                        new_date = start_date + timedelta(days=i)
                        if calendar.day_name[new_date.weekday()] != 'Friday':
                            forecast = self.search(
                                [('product_id', '=', product_id), ('date', '=', str(new_date.date())),
                                 ('mode', '=', 'manual')])
                            qty = (new_quantity_per_day if new_quantity >= new_quantity_per_day else (
                                new_quantity if new_quantity > 0 else 0))
                            if forecast:
                                forecast.to_supply = qty
                            else:
                                self.create(
                                    {'date': str(new_date.date()), 'product_id': product_id, 'to_supply': qty,
                                     'mode': 'manual'})
                            new_quantity -= new_quantity_per_day
