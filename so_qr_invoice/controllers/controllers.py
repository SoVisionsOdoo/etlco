
from odoo.http import content_disposition, route, request, Controller
import io
from odoo import http
import base64

class ApiController(Controller):
    @route('/qr/<int:idit>', auth='public')   # not used
    def index(self, idit):
        invoices = request.env['account.move']
        return request.render('so_qr_invoice.qr_scanned_document', {
                                  'o': invoices.search([('id', '=', idit)])
                               })

    @route('/qr/attachment/download/<int:attach_id>', type='http', auth='public')
    def qr_scanned_download(self, attach_id):
        invoice = request.env['so_qr_invoice.attachment'].sudo().search([('id', '=', attach_id)])
        data = io.BytesIO(base64.standard_b64decode(invoice["datas"]))
        filename = invoice.name + '.pdf'

        return http.send_file(data, filename=filename, as_attachment=True)
