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
    def btn_reject(self, vals):
        for rec in self:
            rec.write({'status': 'reject'})

#    @api.multi
#    def btn_close(self, vals):
#        for rec in self:
#            rec.write({'status': 'close'})
#            komersial = self.env['komersial.komersial'].create({
#                'name': rec.id,
#                'cust_id': rec.cust_id.id,
#                'dok_basp': rec.dok_basp,
#                'dok_bakr': rec.dok_bakr,
#                'komersial_line_ids': rec.workorders_line_ids,
#                })
            # for rec2 in rec.workorders_line_ids.filtered (lambda x: not x.workorders_id):
            #     komersial_line = self.env['komersial.line'].create({
            #         'name': rec2.id,
            #         })

    @api.multi
    def btn_close(self, vals):
        for rec in self:
            rec.write({'status': 'close'})
            komersial = self.env['komersial.komersial'].create({
                'name': rec.id,
                'cust_id': rec.cust_id.id,
                'dok_basp': rec.dok_basp,
                'dok_bakr': rec.dok_bakr,
                })
            workorders_line = self.env['workorders.line'].search([('workorders_id','=',rec.id)])
#            workorders_line = self.env['workorders.line'].search([])
            for line in workorders_line:
                if line.tagihan_ok:
                    komersial_line = self.env['komersial.line'].create({
                        'komersial_id': komersial.id,
                        'id': line.id,
                        'name': line.name.id,
                        'qty': line.qty,
                        'harga_inv': line.name.id.standar_price,
                        })


    @api.model
    def create(self, vals):
        obj = super(Workorders, self).create(vals)
        if obj.name == '/':
            number = self.env['ir.sequence'].get('name.sequence.code') or '/'
            obj.write({'name': number})
        return obj

    name = fields.Char(string="WO#", default='/', readonly=True)
    unit_id = fields.Many2one('unit.unit', string="Unit", required=True)
    wo_oracle = fields.Char(string="WO# Oracle")
    cust_id = fields.Many2one('customer.komersial', string="Customer",related='unit_id.cust_id')
    nama_pekerja = fields.Char(string="Nama Pekerjaan")
    # cabang = fields.Many2one("stock.warehouse",string="Cabang")
    status = fields.Selection([
    	('draft', 'Draft'),
        ('waiting', 'Waiting'),
        ('approved', 'Approved'),
        ('reject', 'Reject'),
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

    name = fields.Many2one("product.template", string="Product", required=True)
    uom = fields.Char(string="UoM", related='name.uom_id.name')
    qty = fields.Float(string="Qty")
    tagih_ok = fields.Boolean(string="Ditagihkan") 
    lokal_ok = fields.Boolean(string="Lokal") 
    harga_lokal = fields.Float(string="Harga Lokal")
    workorders_id = fields.Many2one("workorders.workorders", string="Workorders Id")

class UnitUnit(models.Model):
    _name ='unit.unit'
    _description = 'Units'

    name = fields.Char(string="Name", required=True)

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
    type_lokasi = fields.Selection([
        ('parent', 'Parent'),
        ('child', 'Child'),
        ], string='Status', store=True, default="child")

class GroupAlat(models.Model):
    _name = 'group.alat'
    _description = 'Group Alat'

    name = fields.Char(string="Group Alat")

class CustPrice(models.Model):
    _name = 'cust.price'
    _description = 'Customer Price'

    price = fields.Float(string="Price")
    name = fields.Many2one('customer.komersial', string="Customer")
    product_id = fields.Many2one('product.template', string="Product Id")

