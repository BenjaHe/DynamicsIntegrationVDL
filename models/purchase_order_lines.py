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
    # dyn_taxgroup_id = fields.Char(related='product_id.dyn_taxgroup',
    #                               string="Champs TaxGroup issu de Dynamics",
    #                               required=False)
    #
    # dyn_taxitemgroup_id = fields.Char(related='product_id.dyn_taxitemgroup',
    #                                   string="Champs TaxGroup issu de Dynamics",
    #                                   required=False)

    dyn_purchid = fields.Integer(string="Champs PurchID dans Dynamics",
                                 required=False)

    dyn_liberer = fields.Boolean()

    # Statut spécifique Dyn. -> au quel on a ajouté deux statuts (pending et no_sync) pour "taguer" les PO
    # qu'il ne faut pas ou qu'il faut synchroniser (pour retenir les PO générés par les règles de réappro).
    # En lien avec purchase_order_line_stage qui configure les statuts Odoo VS Dyn
    stage_id = fields.Many2one(
        comodel_name="purchase.order.line.stage",
        default=lambda self: self.env['purchase.order.line.stage'].search(
            [('dyn_status', '=', 'odoo_no_sync')], limit=1),
        track_visibility='onchange',
    )

    @api.multi
    def action_line_liberer(self):
        pending_sync_status = self.env['purchase.order.line.stage'].search(
            [('dyn_status', '=', 'odoo_pending')], limit=1)
        for line in self:
            if not line.dyn_liberer and line.stage_id and \
                    line.stage_id.dyn_status in ('odoo_no_sync', 'odoo_pending'):
                vals = {
                    'stage_id': pending_sync_status.id,
                    'dyn_liberer': True,
                }
                line.write(vals)
            else:
                msg = u"Ligne: {name}, ".format(name=line.name)
                if line.dyn_liberer:
                    msg += u"déja libérée, "
                if line.stage_id:
                    msg += u"état: {stage_id}".format(
                        stage_id=line.stage_id.name_get()[0][1])
                line.order_id.message_post(body=msg)
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
