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
    dyn_liberer = fields.Boolean(
        string="Peut être poussé vers Dynamics",
    )

    @api.model
    def create(self, vals):
        purchase = super(Purchase, self).create(vals)
        if not purchase.partner_id.fournisseur_economat:
            purchase.action_liberer()
        return purchase

    @api.multi
    def action_liberer(self):
        for po in self:
            if not po.dyn_liberer:
                vals = {
                    'dyn_liberer': True,
                }
                po.write(vals)
            else:
                msg = "Commande déjà libérée"
                po.message_post(body=msg)
        return True

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
