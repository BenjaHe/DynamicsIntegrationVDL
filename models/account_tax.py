# -*- coding: utf-8 -*-

from openerp import models, fields, api


class AccountTax(models.Model):
    _inherit = 'account.tax'

    # Id de la taxe - taxgroup - de l'article dans Microsoft Dyn (utilisé pour pousser les commandes dans Dyn)
    dyn_taxgroup = fields.Char(
        string="Champs TaxGroup issu de Dynamics",
        required=False,
    )

    # Id de la taxe - taxitemgroup - de l'article dans Microsoft Dyn (utilisé pour pousser les commandes dans Dyn)
    dyn_taxitemgroup = fields.Char(
        string="Champs TaxItemGroup issu de Dynamics",
        required=False,
    )

    # Méthode appelée pour l'affichage des référencess
    # nous allon ajouter le dyn_taxgroup au no par défaut pour afficher ce
    # dernier dans le champ Many2one, One2many et Many2many
    # qui référence des account.tax
    @api.multi
    def name_get(self):
        res = super(AccountTax, self).name_get()
        result = []
        for tuple in res:
            tax = self.browse(tuple[0])
            tuple_id = tuple[0]
            tuple_name = tuple[1]
            if tax.dyn_taxgroup:
                tuple_name = "{name} [{dyn_taxgroup}]".format(
                    name=tuple_name, dyn_taxgroup=tax.dyn_taxgroup)
            new_tuple = (tuple_id, tuple_name)
            result.append(new_tuple)
        return result

    # Méthode appelée lorsqu'on recherche un account.tax dans un champ Many2one,
    # One2many et Many2mnay
    # Ici nous voulons que l'utilisateur puisse rechercher une tax par le code
    # "dyn_taxgroup"
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name),
                      ('dyn_taxgroup', operator, name)]
        pos = self.search(domain + args, limit=limit)
        return pos.name_get()
