# -*- coding: utf-8 -*-


from datetime import date, datetime, timedelta
from openerp import models, fields, api, exceptions
from openerp.addons.website_sale.models.product import product_public_category
from openerp.exceptions import Warning

class Product(models.Model):
    _inherit = ['product.template']

    # Id de la taxe - taxgroup - de l'article dans Microsoft Dyn (utilisé pour pousser les commandes dans Dyn)
    dyn_taxgroup = fields.Char(string="Champs TaxGroup issu de Dynamics",
                               required=False)

    # Id de la taxe - taxitemgroup - de l'article dans Microsoft Dyn (utilisé pour pousser les commandes dans Dyn)
    dyn_taxitemgroup = fields.Char(string="Champs TaxGroup issu de Dynamics",
                                   required=False)

