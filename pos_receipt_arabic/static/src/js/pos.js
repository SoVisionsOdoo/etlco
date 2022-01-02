odoo.define('pos_receipt_arabic.pos', function(require) {
    "use strict";
    var PosBaseWidget = require('point_of_sale.chrome');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var utils = require('web.utils');
    var round_di = utils.round_decimals;

    var QWeb = core.qweb;
    console.log("PosBaseWidget", PosBaseWidget)

    var models = require('point_of_sale.models');

//    models.load_fields('pos.config',['allow_qr_code']);

    var module = require('point_of_sale.models');
    var models = module.PosModel.prototype.models;
    for(var i=0; i<models.length; i++){
        var model=models[i];
        if(model.model === 'res.company'){
             model.fields.push('street', 'city', 'state_id', 'country_id');
        }
    }

    screens.ReceiptScreenWidget.include({
    render_receipt: function() {
        var self = this;
        this._super();
        let order = this.pos.get_order();
        var qr_code_data = "Company:"+this.pos.company.name;
        if(this.pos.company.vat){
             qr_code_data += "  | VAT NO.:"+ this.pos.company.vat;
        }
        if(order['formatted_validation_date']){
            qr_code_data += "  | Order Date:"+ order['formatted_validation_date'];
        }
        if(order.get_total_with_tax()){
            qr_code_data += "  | Total Amount:"+ Math.round(order.get_total_with_tax() * 100)/100;
        }
        if(order.get_total_tax()){
            qr_code_data += "  | Total Tax:"+ Math.round(order.get_total_tax() * 100)/100;
        }
        // console.log(qr_code_data);
        // self.qr_code = qr_code_data;
        // new QRCode(document.getElementById("qrcode"), {"text": qr_code_data ,width:200, height:200, correctLevel : QRCode.CorrectLevel.H});
    },
  });

});
