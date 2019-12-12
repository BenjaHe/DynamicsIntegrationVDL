# -*- coding: utf-8 -*-


from datetime import date, datetime, timedelta
from openerp import models, fields, api, exceptions
from openerp.addons.website_sale.models.product import product_public_category
from openerp.exceptions import Warning

class ResPartner(models.Model):
    _inherit = ['res.partner']

    # Champs Dynamics qui donne les références Dyn du fournisseur
    # dyn_buyergroupid = fields.Char(string='Numéro du comptable dans Dynamics',
    #                                required=False,
    #                                track_visibility='onchange',
    #                                help='A renseigner uniquement pour les comptables.')

    mon_dyn_buyergroupid = fields.Char(string='Numéro de mon comptable dans Dynamics',
                                       required=False,
                                       related='comptable.dyn_buyergroupid',
                                       help='Le numéro du comptable dans Dynamics qui m est renseigné.')

    dyn_orderaccount = fields.Char(string='Numéro du fournisseur dans Dynamics',
                                   required=False,
                                   help='Vient automatiquement')