
from odoo.http import content_disposition, route, request, Controller
from odoo.addons.web.controllers import main as report
from odoo import http
import base64
import io


class CustomController(report.ReportController):
    @route(['/report/download'], type='http', auth="user")
    def report_download(self, data, token, context=None):
        res = super(CustomController, self).report_download(data, token, context)
        print(data)
        if len(data.split('/')) == 5:  # means it's in the form --> /report/pdf/model/id
            model = data.split('/')[3].split(".")[0]
            report_type = data.split('/')[3].split(".")[1]
            activeId = data.split('/')[4].split("\"")[0]
        else:
            return res

        # Customizable according to the required reports and models
        if model in ['account','de_print_journal_entries','so_invoice_report','so_esh_hza_e_invoice'] \
                and report_type in ['report_invoice_with_payments', 'report_invoice','journal_entries_report_template','customer_einvoice_report_ar','customer_e_invoice_report_esh_haza'] \
                and activeId:
            move = request.env['account.move'].sudo().search([('id', '=', int(activeId))])  # Check existence of move
        else:
            return res

        if not move:
            return res

        attachment = {
            'datas': base64.encodebytes(res.data),
            'type': 'binary',
            'name': move.name,
            'res_model': 'account.move',
            'res_id': int(activeId),
            'attach_model': model,
            'attach_type': report_type
        }
        current_attachment = request.env['so_qr_invoice.attachment'].sudo().search([('res_id', '=', int(activeId)),
                                                                                     ('attach_model', '=', model),
                                                                                     ('attach_type', '=', report_type)])
        if current_attachment:
            print('write')
            current_attachment.sudo().write(attachment)
        else:
            print('create')
            request.env['so_qr_invoice.attachment'].create(attachment)
        res = super(CustomController, self).report_download(data, token, context)
        return res


