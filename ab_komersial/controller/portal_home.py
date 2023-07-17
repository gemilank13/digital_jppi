from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request
from odoo import http

class WebKomersialPortalHome(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(WebKomersialPortalHome, self)._prepare_portal_layout_values()
        komersial_count_tmp = 0
        if request.env['komersial.komersial'].check_access_rights('read', raise_exception=False):
            # partner_id = request.env.user.partner_id.id
            komersial_count_tmp = request.env['komersial.komersial'].search_count([])
        komersial_count = komersial_count_tmp
        values['komersial_count'] = komersial_count
        return values