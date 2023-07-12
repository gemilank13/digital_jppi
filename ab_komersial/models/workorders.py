# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class Workorders(models.Model):
    _name = 'workorders.workorders'
    _description = 'Work Orders'

    @api.multi
    def btn_submit(self, vals):
        for rec in self:
            rec.write({'status': 'waiting'})

    @api.multi
    def btn_approved(self, vals):
        for rec in self:
            rec.write({'status': 'approved'})

    @api.multi
    def btn_close(self, vals):
        for rec in self:
            rec.write({'status': 'close'})



    @api.model
    def create(self, vals):
        obj = super(Workorders, self).create(vals)
        if obj.name == '/':
            number = self.env['ir.sequence'].get('name.sequence.code') or '/'
            obj.write({'name': number})
        return obj

    name = fields.Char(string="WO#", default='/', readonly=True)
    unit_id = fields.Many2one('unit.unit', string="Unit")
    wo_oracle = fields.Char(string="WO# Oracle")
    cust_id = fields.Many2one('customer.komersial', string="Customer",related='unit_id.cust_id')
    nama_pekerja = fields.Many2one('hr.employee', string="Nama Pekerjaan")
    cabang = fields.Many2one("stock.warehouse",string="Cabang")
    status = fields.Selection([
    	('draft', 'Draft'),
        ('waiting', 'Waiting'),
        ('approved', 'Approved'),
        ('close', 'Close'),
        ], string='Status', store=True, default="draft")
    tanggal = fields.Datetime(string="Tanggal")
    workorders_line_ids = fields.One2many("workorders.line", "workorders_id", string="Work Orders Line")
    dok_basp = fields.Char(string="BASP#")
    dok_bakr = fields.Char(string="BAKR#")
    date_selesai = fields.Datetime(string="Tanggal Selesai Pekerjaan")




class WorkordersLine(models.Model):
    _name ='workorders.line'
    _description = 'Work Order Line'

    name = fields.Many2one("product.product", string="Product")
    uom = fields.Char(string="UoM")
    qty = fields.Float(string="Qty")
    tagih_ok = fields.Boolean(string="Ditagihkan") 
    lokal_ok = fields.Boolean(string="Lokal") 
    harga_lokal = fields.Float(string="Harga Lokal")
    workorders_id = fields.Many2one("workorders.workorders", string="Workorders Id")

class UnitUnit(models.Model):
    _name ='unit.unit'
    _description = 'Units'

    name = fields.Char(string="Name")

    def _compute_asset(self):
        for rec in self:
            rec.asset_number = rec.name

    asset_number = fields.Char(string="Asset Number", compute="_compute_asset")
    group_alat = fields.Many2one('group.alat',string="Group Alat")
    cust_id = fields.Many2one('customer.komersial', string="Customer")

class CustomerKomersial(models.Model):
    _name = 'customer.komersial'
    _description = 'Customer Komersial'

    name = fields.Char(string="Lokasi / Customer")

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s %s' % (rec.parent_id.name or '',rec.name)))
        return result
    parent_id = fields.Many2one('customer.komersial', string="Parent Lokasi")

class GroupAlat(models.Model):
    _name = 'group.alat'
    _description = 'Group Alat'

    name = fields.Char(string="Group Alat")
