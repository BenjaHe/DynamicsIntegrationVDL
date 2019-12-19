# -*- encoding: utf-8 -*-

from openerp import api, SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)


def auto_liberer_purchase_order(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    domain = [
        ('state', 'not in', ('purchase', 'done', 'cancel')),
        ('fournisseur_economat', '=', False),
    ]
    orders = env['purchase.order'].search(domain)
    orders.action_liberer()


def migrate(cr, version):
    if not version:
        return
    _logger.info("*****   Starting DynamicsIntegrationVDL upgrade to 9.0.1.0.1 post migration *************")
    auto_liberer_purchase_order(cr)
    _logger.info("***** END DynamicsIntegrationVDL migration complete *************")
    return
