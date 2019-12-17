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
    dyn_update_state_error_message = fields.Char(
        string="Erreur d'update automatique du status",
        help='Error message if the function update_state_from_dyn goes '
             'in exception'
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
            to_state = list(set(to_state))
            if len(to_state) == 1:
                to_state = to_state[0]
                try:
                    order.update_state_conditions(to_state=to_state)
                    order.dyn_update_state_error_message = ""
                except Exception, e:
                    order.dyn_update_state_error_message = e
                    order.message_post(body=e)

    def update_state_conditions(self, to_state):
        # TODO: update le state
        # ('draft', 'Draft PO'),
        # ('sent', 'RFQ Sent'),
        # ('validation_1', 'BdC à envoyer'),
        # ('to approve', 'To Approve'),
        # ('purchase', 'Purchase Order'),
        # ('done', 'Done'),
        # ('cancel', 'Cancelled')
        if to_state == 'draft' and self.state != 'draft':
            if self.state in \
                    ('draft', 'sent', 'validation_1', 'to approve'):
                # Noting to do
                pass
            elif self.state in ('purchase', 'done'):
                self.button_cancel()
                self.button_draft()
            elif self.state == 'cancel':
                self.button_draft()
        elif to_state == 'sent' and self.state != 'sent':
            if self.state in \
                    ('draft', 'sent', 'validation_1', 'to approve'):
                # Noting to do
                pass
            elif self.state in ('purchase', 'done'):
                self.button_cancel()
                self.button_draft()
                self.write({'state':'sent'})
            elif self.state == 'cancel':
                self.button_draft()
                self.write({'state': 'sent'})
        elif to_state == 'validation_1' and self.state != 'validation_1':
            if self.state in ('draft', 'sent', 'to approve'):
                self.action_to_validation_1()
            elif self.state in ('purchase', 'done'):
                self.button_cancel()
                self.button_draft()
                self.action_to_validation_1()
            elif self.state == 'cancel':
                self.button_draft()
                self.action_to_validation_1()
        elif to_state == 'to approve' and self.state != 'to approve':
            if self.state in \
                    ('draft', 'sent', 'validation_1', 'cancel'):
                self.action_to_validation_1()
            elif self.state in ('purchase', 'done'):
                self.button_cancel()
                self.button_draft()
                self.action_to_validation_1()
        elif to_state == 'purchase' and self.state != 'purchase':
            if self.state in \
                    ('draft', 'sent', 'validation_1', 'to approve'):
                self.button_confirm()
            elif self.state == 'done':
                # do nothing
                pass
            elif self.state == 'cancel':
                self.button_draft()
                self.button_confirm()
        elif to_state == 'done' and self.state != 'done':
            if self.state in \
                    ('draft', 'sent', 'validation_1', 'to approve', 'purchase'):
                self.button_confirm()
                self.button_done()
            elif self.state == 'purchase':
                self.button_done()
            elif self.state == 'cancel':
                # do nothing
                pass
            elif self.state == 'cancel':
                self.button_draft()
                self.button_confirm()
                self.button_done()
        elif to_state == 'cancel' and self.state != 'cancel':
            self.button_cancel()

    @api.depends('order_line', 'order_line.dyn_liberer')
    def _compute_dyn_liberer(self):
        for po in self:
            po.dyn_liberer = any(dyn_liberer for dyn_liberer in
                                 po.order_line.mapped('dyn_liberer'))
