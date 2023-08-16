# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class KomersialKomersial(models.Model):
    _name = 'komersial.komersial'
    _description = 'Komersial'

    @api.multi
    def sent_svp(self, vals):
        for rec in self:
            rec.write({'status': 'waiting'})

    # Approve SVP
    @api.multi
    def sent_cust(self, vals):
        for rec in self:
            rec.write({'status': 'sent'})

    @api.multi
    def approve_cust(self, vals):
        for rec in self:
            rec.write({'status': 'approved'})

    @api.multi
    def negotiation_cust(self, vals):
        for rec in self:
            rec.write({'status': 'negotiation'})


    name = fields.Many2one('workorders.workorders', string="WO#")
    komersial_line_ids = fields.One2many("komersial.line", "komersial_id", string="Komersial Line")
    cust_id = fields.Many2one('customer.komersial', string="Customer")
    wo_oracle = fields.Char(string="WO# Oracle")
    dok_basp = fields.Char(string="BASP#")
    dok_bakr = fields.Char(string="BAKR#")

    @api.model
    def create(self, vals):
        obj = super(KomersialKomersial, self).create(vals)
        if obj.tagihan == '/':
            number = self.env['ir.sequence'].get('tagihan.sequence.code') or '/'
            obj.write({'tagihan': number})
        return obj

    tagihan = fields.Char('No. Tagihan', default='/', readonly=True)
    status = fields.Selection([
        ('new', 'New'),
        ('waiting', 'Waiting'),
        ('sent', 'Sent'),
        ('negotiation', 'Negotiation'),
        ('approved', 'Approved'),
        ('in progress', 'In Progress'),
        ('done', 'Done'),
        ], string='Status', store=True, default="new")

class KomersialLine(models.Model):
    _name = 'komersial.line'
    _description = 'Komersial Line'

    name = fields.Many2one("product.template", string="Product", required=False)
    product_type_id = fields.Many2one("komersial.product.type", string="Product Type")
    komersial_id = fields.Many2one("komersial.komersial", string="Komersial Id")
    harga_jual = fields.Float(string="Harga Jual")
    harga_nego = fields.Float(string="Harga Negosiasi")
    harga_inv = fields.Float(string="Harga Inventory")
    qty = fields.Float(string="Qty")
    harga_kesepakatan = fields.Float(string="Harga Kesepakatan")

    @api.depends('qty','harga_jual')
    def _compute_subtotal(self):
        for rec in self:
            rec.sub_total = rec.qty * rec.harga_jual

    sub_total = fields.Float(string="Sub Total", compute='_compute_subtotal', store=True, readonly=True, track_visibility='always')

class KomersialProductType(models.Model):
    _name = 'komersial.product.type'
    _description = 'Komersial Product Type'

    name = fields.Char(string="Product Type")
