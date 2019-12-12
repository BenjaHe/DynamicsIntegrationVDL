# -*- coding: utf-8 -*-

from openerp import api, fields, models

class PurchaseOrderline(models.Model):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
    _description = "Purchase Line Custom for Microsoft Dynamics"

    dyn_orderaccount_id = fields.Char(related='order_id.dyn_orderaccount',
                                      string="Id Dyn du fournisseur",
                                      required=False)
    dyn_buyergroupid_id = fields.Char(related='order_id.dyn_buyergroupid_id',
                                       string="Comptable dans Dynamics",
                                       required=False)
    dyn_taxgroup_id = fields.Char(related='product_id.dyn_taxgroup',
                              string="Champs TaxGroup issu de Dynamics",
                              required=False)

    dyn_taxitemgroup_id = fields.Char(related='product_id.dyn_taxitemgroup',
                               string="Champs TaxGroup issu de Dynamics",
                               required=False)

    dyn_state = fields.Selection([('None', 'Brouillon'),
                                  ('Backorder', 'Bon de commande créé'),
                                  ('Received', 'Commande reçue par le fournisseur'),
                                  ('Invoiced', 'En cours de livraison'),
                                  ('Canceled','Annulé')],
                                  string='Statut Dynamics de la ligne',
                                  default='None',
                                  store=True,
                                  track_visibility='onchange')

    dyn_purchid = fields.Integer(string="Champs PurchID dans Dynamics",
                                 required=False)

    order_dyn_liberer = fields.Boolean(
        related='order_id.dyn_liberer',
        store=True,
    )

    # Statut spécifique Dyn. -> au quel on a ajouté deux statuts (pending et no_sync) pour "taguer" les PO
    # qu'il ne faut pas ou qu'il faut synchroniser (pour retenir les PO générés par les règles de réappro).
    # En lien avec purchase_order_line_stage qui configure les statuts Odoo VS Dyn
    stage_id = fields.Many2one(
        comodel_name="purchase.order.line.stage",
        default=lambda self: self.env['purchase.order.line.stage'].search(
            [('dyn_status', '=', 'odoo_no_sync')], limit=1),
    )

    @api.model
    def create(self, vals):
        line = super(PurchaseOrderline, self).create(vals)
        if line.order_dyn_liberer:
            line.action_line_libeter()
        return line

    @api.multi
    def write(self, vals):
        res = super(PurchaseOrderline, self).write(vals)
        if vals.get('order_dyn_liberer', False):
            self.action_line_libeter()
        return res

    @api.multi
    def action_line_libeter(self):
        pending_sync_status = self.env['purchase.order.line.stage'].search(
            [('dyn_status', '=', 'odoo_pending')], limit=1)
        for line in self:
            if line.order_dyn_liberer and line.stage_id and \
                    line.stage_id.dyn_status == 'odoo_no_sync':
                vals = {
                    'stage_id': pending_sync_status.id,
                }
                line.write(vals)
            else:
                msg = "Ligne: {name}, "
                if line.order_dyn_liberer:
                    msg += "déja libérée, "
                msg += "état: {stage_id}"
                msg.format(name=line.name, stage_id=line.stage_id)
                line.order_id.message_post(body=msg)
        return True
