# -*- coding: utf-8 -*-
{
    'name': "Dynamics Integration VDL",

    'summary': """
        Extention du module StockVDL pour l'intégration avec Dynamics.""",

    'description': """
        Le module ajoute les informations nécessaires (champs) pour pousser automatiquement les commandes webshop
        dans Microsoft Dynamics. Le protocole d'échange se basant sur des fichiers CSV, seuls des champs on été ajouté
        mais aucun export n'a été programmé.

    """,

    'author': "Roland Neyrinck - DSI Ville de Liège",
    'website': "",

    'category': 'Uncategorized',
    'version': '9.0.1.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','stockVDL'],

    'data': [
        'views/account_tax.xml',
        'views/purchase_order_line_stage.xml',
        'views/purchase_order.xml',
        'views/menu.xml',
        'datas/purchase_order_line_stage.xml',
        'views/res_partner.xml'
             ],

}

