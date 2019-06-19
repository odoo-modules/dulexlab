odoo.define('bi_mrp_mps_customization.mrp_mps_report', function (require) {
'use strict';

var session = require('web.session');
var data = require('web.data');
var field_utils = require('web.field_utils');

var mrp = require('mrp_mps.mrp_mps_report');

var mrp_mps_report = mrp.include({
    events:{
        'change .o_mps_save_input_text': 'mps_forecast_save',
        'change .o_mps_save_input_supply': 'on_change_quantity',
        'click .open_forecast_wizard': 'mps_open_forecast_wizard',
        'click .o_mps_apply': 'mps_apply',
        'click .o_mps_add_product': 'add_product_wizard',
        'click .o_mps_generate_procurement': 'mps_generate_procurement',
        'mouseover .o_mps_visible_procurement': 'visible_procurement_button',
        'mouseout .o_mps_visible_procurement': 'invisible_procurement_button',
        'click .o_mps_product_name': 'open_mps_product',},
    mps_forecast_save: function(e){
        var self = this;
        var $input = $(e.target);
        var target_value;
        try {
            target_value = field_utils.parse.integer($input.val().replace(String.fromCharCode(8209), '-'));
        } catch(err) {
            return this.do_warn(_t("Wrong value entered!"), err);
        }
        return this._rpc({
            model: 'sale.forecast',
            method: 'save_forecast_data',
            args: [parseInt($input.data('product')), target_value, $input.data('date'), $input.data('date_to'),
             $input.data('name'), self.report_context.period],
            kwargs: {context: session.user_context},
        })
        .done(function(res){
            self.get_html().then(function() {
                self.re_renderElement();
            });
        });
    },


    });
});