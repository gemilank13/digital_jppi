# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from dateutil.relativedelta import relativedelta


class RekapReportWizard(models.TransientModel):
    _name = 'rekap.report.wizard'

    date_start = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(string="End Date", required=True, default=fields.Date.today)
    report_type = fields.Selection([
        ('rekapitulasi', 'Rekapitulasi'),
        ('summary', 'Summary'),
        ], string='Report Type', store=True, default="rekapitulasi")
    cust_id = fields.Many2one('customer.komersial',string="Lokasi/Customer")

    @api.multi
    def get_report(self):
        """Call when button 'Get Report' clicked.
        """
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
                'report_type': self.report_type,
                'cust_id': self.cust_id.name,
            },
        }

        # use `module_name.report_id` as reference.
        # `report_action()` will call `_get_report_values()` and pass `data` automatically.
        return self.env.ref('ab_komersial_report.rekap_report').report_action(self, data=data)


class ReportRekapReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.ab_komersial_report.rekap_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        report_type = data['form']['report_type']
        cust_id = data['form']['cust_id']
        date_start_obj = datetime.strptime(date_start, DATE_FORMAT)
        date_end_obj = datetime.strptime(date_end, DATE_FORMAT)
        date_diff = (date_end_obj - date_start_obj).days + 1

        docs = []
        rekap = self.env['komersial.komersial'].search([
            ('name.date_selesai', '>=', date_start_obj.strftime(DATETIME_FORMAT)),
            ('name.date_selesai', '<=', date_end_obj.strftime(DATETIME_FORMAT)),
        ])
        for rk in rekap:
            # total = date_diff * 24
            # total_dt = (pd.end_date - pd.start_date).days + 1
            # avala = (total - total_dt)/total * 100
            docs.append({
                'name': pd.name
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'cust_id':cust_id,
            'docs': docs,
        }

