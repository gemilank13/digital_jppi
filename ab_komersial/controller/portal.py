from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request
from odoo import http

class WebKomersialPortal(CustomerPortal):

	@http.route('/my/customer', type='http', website=True)
	def WebKomersialListView(self, **kw):
		print("SUCCESSSSSSS")
		komersial_obj = request.env['komersial.komersial']
		komersial = komersial_obj.search([])
		vals = {'komersial':komersial, 'page_name':'customer_list_view'}
		return request.render("ab_komersial.web_customer_list_view_portal", vals)