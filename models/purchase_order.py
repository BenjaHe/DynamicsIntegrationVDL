# -*- coding: utf-8 -*-


from datetime import date, datetime, timedelta
from openerp import models, fields, api, exceptions
from openerp.exceptions import Warning

class Purchase(models.Model):
    _inherit = ['purchase.order']


    dyn_orderaccount = fields.Char(
        related='partner_id.dyn_orderaccount',
        string='Num Dynamics du fournisseur',
        readonly=True,
        required=False,
    )

    dyn_buyergroupid_id = fields.Char(
        "res.users",
        related='dest_address_id.comptable.dyn_buyergroupid',
        readonly=True,
        required=False,
    )

    # Indicateur qui dit si le Purchase Order peut-être poussé dans Dynamics car il ne faut pas pousser
    # automatiquement les PO qu sont générés par le système pour réapprovisionner le stock !
    # --> il faut attendre que l'Economat donne son go une fois que le PO est suffisamment rempli.
    dyn_liberer = fields.Boolean(compute='_compute_liberer', string="Peut être poussé vers Dynamics")



    # Méthode qui définit la valeur de dyn_liberer
    # @api.multi
    # @api.depends('fournisseur_economat')
    # def _compute_liberer(self):
    #     for rec in self:
    #         if self.fournisseur_economat : False
    #         return True
    #
    #         else self.fournisseur_economat : True
    #         return False


        # ajout changement du tag quand clic sur bouton (à créer) mais ! qu'il ne faut pas retomber sur la tag d'origine (=fournisseur_economat)

    def export_to_dynamics(self):
        values = {'test': True}
        domain = []
        return values

    def import_from_dynamics(self, values):
        result = True
        try:
            pass
        except:
            result = False
        return result
