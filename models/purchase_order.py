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
        compute='_compute_dyn_liberer',
        store=True
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
            po.order_line.action_line_liberer()
            if po.state == 'draft':
                # update du state de 'draft' à 'sent' pour que les nouvelles
                # lignes de commandes ne soient plus ajouté à cette commande,
                # mais qu'une nouvelle commande (avec dyn_liberer=False)
                # soit générée par Odoo
                po.state = 'sent'
        return True

    @api.multi
    def update_state_from_dyn(self):
        for order in self:
            to_state = order.mapped('order_line.stage_id.po_state')
            if len(to_state) == 1:
                #TODO: update le state
                pass

    @api.depends('order_line', 'order_line.dyn_liberer')
    def _compute_dyn_liberer(self):
        for po in self:
            po.dyn_liberer = any(dyn_liberer for dyn_liberer in
                                 po.order_line.mapped('dyn_liberer'))
