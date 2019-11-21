# -*- coding: utf-8 -*-


from openerp import models, fields, api
from openerp.exceptions import Warning

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

    @api.multi
    def write(self, vals):
        for rec in self:
            if rec.dyn_status in ('odoo_pending', 'odoo_no_sync'):
                raise Warning(
                    "Vous ne pouvez pas modifier les deux premiers status")
        return super(PurchaseOrderLineStage, self).write(vals)

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.dyn_status in ('odoo_pending', 'odoo_no_sync'):
                raise Warning(
                    "Vous ne pouvez pas supprimer les deux premiers status")
        return super(PurchaseOrderLineStage, self).unlink()
