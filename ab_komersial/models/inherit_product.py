# -*- coding: utf-8 -*-
from odoo import models, fields, api

class InheritProduct(models.Model):
    _inherit = 'product.template'

    custprice_line_ids = fields.One2many('cust.price', 'product_id', string="Customer Price")