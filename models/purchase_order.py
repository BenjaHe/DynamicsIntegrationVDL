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
        return True

    @api.depends('order_line', 'order_line.dyn_liberer')
    def _compute_dyn_liberer(self):
        for po in self:
            po.dyn_liberer = any(dyn_liberer for dyn_liberer in
                                 po.order_line.mapped('dyn_liberer'))

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
