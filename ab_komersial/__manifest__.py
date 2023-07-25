# -*- coding: utf-8 -*-
{
    'name': "JPPI - Komersial",

    'summary': """ Modul Dokumen Komersial """,
    'description': """ Modul Dokumen Komersial """,
    'author': "PT JPPI - Geger Gemilank",
    'website': "http://www.pelindoportequipment.jppi.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','hr','stock','portal','product'],

    'data': [
         'security/security.xml',
         'security/ir.model.access.csv',
         'views/komersial_komersial.xml',
         'views/komersial_customer.xml',
         'views/workorders.xml',
         'views/portal_template.xml',
         'views/portal_home.xml',
         'views/sequence.xml',
         'views/inherit_users.xml',
         'views/inherit_product.xml',
    ],
    
    'demo': [],
}