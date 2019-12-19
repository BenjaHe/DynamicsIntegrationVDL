# -*- encoding: utf-8 -*-

from openerp import api, SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)


def auto_liberer_purchase_order(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    domain = [
        ('dyn_state','=','None'),  # on cherche toutes les lines qui ont un dyn_state = None
    ]
    order_lines = env['purchase.order.line'].search(domain)
    order_lines.write({'dyn_state':''}) # et toutes les lignes qu'on a trouvées, on leur écrit un statut vide
    # (car on exporte que celle qui n'ont pas encore de statut dy)



def migrate(cr, version):
    if not version:
        return
    _logger.info("*****   Starting DynamicsIntegrationVDL upgrade to 9.0.1.0.2 post migration *************")
    auto_liberer_purchase_order(cr)
    _logger.info("***** END DynamicsIntegrationVDL migration complete *************")
    return
