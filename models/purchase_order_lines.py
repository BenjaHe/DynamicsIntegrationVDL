# -*- coding: utf-8 -*-

from openerp import api, fields, models

class PurchaseOrderline(models.Model):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
    _description = "Purchase Line Custom for Microsoft Dynamics"

    # dyn_orderaccount_id = fields.Char(related='order_id.dyn_orderaccount',
    #                                   string="Id Dyn du fournisseur",
    #                                   required=False)
    # dyn_buyergroupid_id = fields.Char(related='order_id.dyn_buyergroupid_id',
    #                                    string="Comptable dans Dynamics",
    #                                    required=False)
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

    # Statut spécifique Dyn. -> au quel on a ajouté deux statuts (pending et no_sync) pour "taguer" les PO
    # qu'il ne faut pas ou qu'il faut synchroniser (pour retenir les PO générés par les règles de réappro).
    # En lien avec purchase_order_line_stage qui configure les statuts Odoo VS Dyn
    stage_id = fields.Many2one(
        comodel_name="purchase.order.line.stage",
    )
