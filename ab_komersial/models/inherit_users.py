# -*- coding: utf-8 -*-
from odoo import models, fields, api

class InheritUsers(models.Model):
    _inherit = 'res.users'

    lokasi_id = fields.Many2one('res.partner', string="Lokasi Cabang")