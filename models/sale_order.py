# -*- coding: utf-8 -*-


from datetime import date, datetime, timedelta
from openerp import models, fields, api, exceptions
from openerp.addons.website_sale.models.product import product_public_category
from openerp.exceptions import Warning

class Sale(models.Model):
    _inherit = ['sale.order']

    dyn_orderaccount = fields.Char(related='partner_id.dyn_orderaccount',
                                   string='Num Dynamics du fournisseur',
                                   readonly=True,
                                   required=False)

    dyn_buyergroupid_id = fields.Char("res.users",
                                      related='partner_shipping_id.comptable.dyn_buyergroupid',
                                      readonly=True,
                                      required=False)
