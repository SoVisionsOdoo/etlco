odoo.define("pos_receipt_arabic.models", function (require) {
"use strict";

var models = require('point_of_sale.models');

models.load_fields('res.company', ['street','street2','city','state_id','vat']);
})