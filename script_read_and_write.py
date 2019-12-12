# /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

# SCRIPT pour updater Odoo sur base des informations lues dans les fichiers CSV envoyés pas Dyn
# Pour créer un cron Linux : voir le site crontab.guru
# exemple de cron à inscrire dans crontab : 0 5 * * sat /home/addons/monscript.py get /home/export/monfichier.csv ;
# ouvrir crontab : crontab -e

# Ici, on utilise odoorpc donc on ne doit pas définir ce qu'on donne comme exemple sur le site d'Odoo pour les API
# On ne fait que read

import logging
import sys
from datetime import date, timedelta

import odoorpc

_logger = logging.getLogger(__name__)


class CsvToOdooToCsv(object):
    def __init__(self, argvs):
        self.argvs = argvs
        # notice: parent class was like that: "parenet_class.ClassName2"
        self.db = 'copie_prod_13nov2019'
        self.username = 'admin'
        self.password = 'taivoN78'
        self.host = "192.168.232.47"
        self.port = 8069
        self.odoo_connect = self.connect()
        self.file_path = argvs[2]
        self.separator = argvs[3]
        self.columns_mapping = [('id', 'PurchLineID'),
                                ('display_name', 'ExternalitemID'),
                                ('product_qty', 'PurchQty'),
                                ('price_unit', 'PurchPrice'),
                                ('price_tax', 'PurchpriceVAT'),
                                ('taxcode', 'TaxCode')]

    def connect(self):
        odoo = odoorpc.ODOO(host=self.host, port=self.port)
        odoo.login(self.db, self.username, self.password)
        return odoo

    def read_csv(self):   # Pour lire dans le CSV et crée le dictionnaire de valeur qui sera les valeur updatées dans Odoo
        f = open(self.file_path, 'r')
        lines = f.readlines()
        line_nbr = 0
        dico = {}
        for r in lines:
            if line_nbr == 0:
                line_nbr += 1
                continue
            r = r.split(self.separator)
            id = int(r[0])            # il faut prendre d'id qui est en colonne 0
            state = r[1].rstrip()     # on décie de prendre le state qui est en 2° colonne (et comme c'est la dernière, il faut lui mettre  un rstrip
            dico[id] = {'dyn_state': state}
            line_nbr += 1
        f.close()
        return dico

    def write_csv(self, lines): # recoit une liste de liste (ligne) et l'écrit dans le csv
        f = open(self.file_path, 'w')
        for line in lines:
            r = self.separator.join(line)
            f.write(r.encode("utf-8"))
            f.write('\n')
        f.close()

    def read_odoo(self, model_name):
        model_obj = self.odoo_connect.env[model_name]
        delay = date.today() - timedelta(days=200)
        delay = '{}'.format(delay)

        object_ids = model_obj.browse(model_obj.search([('create_date','>=',delay),('fournisseur_economat','=',False)]))
        lines = []
        lines.append([x[1] for x in self.columns_mapping])
        for obj in object_ids:
            row = []
            for col in self.columns_mapping:
                row.append(u'{}'.format(obj[col[0]]))
            lines.append(row)
        return lines

    def write_odoo(self, model_name, dico):
        model_obj = self.odoo_connect.env[model_name]
        for k, v in dico.iteritems():
            model_obj.write([k], v)


if __name__ == "__main__":
    argvs = sys.argv
    instance = CsvToOdooToCsv(argvs)
    action = argvs[1]
    if action == 'get':
        lines = instance.read_odoo('purchase.order.line')
        instance.write_csv(lines)
    if action == 'push':
        dico = instance.read_csv()
        instance.write_odoo('purchase.order.line', dico)