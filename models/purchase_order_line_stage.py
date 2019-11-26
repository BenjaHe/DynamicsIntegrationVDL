# -*- coding: utf-8 -*-


from openerp import models, fields, api
from openerp.exceptions import Warning

# Statut spécifique Dyn. -> au quel on a ajouté deux statuts (pending et no_sync) pour "taguer" les PO
# qu'il ne faut pas ou qu'il faut synchroniser (pour retenir les PO générés par les règles de réappro).
# On a créé deux statuts Dyn en dur dans le code qui sont "odoo_pending" qui bloque les PO en draft
# et "odoo_no_sync" = on peut libérer et pousser dans Dyn mais il n'a pas encore été lu/synchronisé
# par Talend/Dynamics.

# RESTE A FAIRE !!! --> écrire l'algo (bouton) qui dit que si fournisseur Economat -> on met en odoo_pending et
# si ce n'est pas un fournisseur Economat (Bricolux) = on met en odoo_no_sync (statut qui libère le PO mais
# qui n'est pas encore de Dyn.

class PurchaseOrderLineStage(models.Model):
    _name = 'purchase.order.line.stage'

    name = fields.Char(
        string='Name',
        required=True,
    )

    dyn_status = fields.Char(
        string='Status dynamics',
        required=True,
    )

    po_state = fields.Selection(
        string="Purchase state",
        selection=[
            ('draft', 'Draft PO'),
            ('sent', 'RFQ Sent'),
            ('validation_1', 'BdC à envoyer'),
            ('to approve', 'To Approve'),
            ('purchase', 'Purchase Order'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')],
        required=True,
    )

    # On empèche de supprimer ou de unliker les deux statuts indispensables pour savoir si
    # on peut libérer ou pas le PO.
    @api.multi
    def write(self, vals):
        for rec in self:
            if rec.dyn_status in ('odoo_pending', 'odoo_no_sync'):
                raise Warning(
                    "Vous ne pouvez pas modifier les deux premiers status")
        return super(PurchaseOrderLineStage, self).write(vals)

    # On empèche de supprimer ou de unliker les deux statuts indispensables pour savoir si
    # on peut libérer ou pas le PO.
    @api.multi
    def unlink(self):
        for rec in self:
            if rec.dyn_status in ('odoo_pending', 'odoo_no_sync'):
                raise Warning(
                    "Vous ne pouvez pas supprimer les deux premiers status")
        return super(PurchaseOrderLineStage, self).unlink()
