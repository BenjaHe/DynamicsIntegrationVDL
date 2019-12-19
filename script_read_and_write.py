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

import logging, logging.handlers
import sys
from datetime import date, timedelta

import odoorpc

LOGNAME = "odoo_dynamics_script"
#LOGFILE = "/Users/benja/workspace/Projects/Liege_stock/odoo_dynamics_script.log"
LOGFILE = "/var/log/dynamics_odoo_script/doo_dynamics_script.log"
LOGLEVEL = logging.INFO


def openlog(logger, logfile, stdout=False):
    'Opens rotating log file'
    log = logging.getLogger(logger)
    hdlr_file = logging.handlers.RotatingFileHandler(logfile, 'a', 1024 * 1024 * 2, 3)
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s')

    hdlr_file.setFormatter(formatter)

    log.addHandler(hdlr_file)
    if stdout:
        hdlr_stdout = logging.StreamHandler(sys.stdout)
        hdlr_stdout.setFormatter(formatter)
        log.addHandler(hdlr_stdout)

    return log


LOGGER = openlog(LOGNAME, LOGFILE, False)
LOGGER.setLevel(LOGLEVEL)
# Now you can use LOGGER.info("This info")
# Now you can use LOGGER.warning("This info")
# Now you can use LOGGER.error("This info")


class CsvToOdooToCsv(object):
    def __init__(self, argvs):
        self.argvs = argvs
        # notice: parent class was like that: "parenet_class.ClassName2"
        self.db = 'copie_prod_13nov2019'
        self.username = 'admin'
        self.password = 'taivoN78'
        self.host = "192.168.232.47"
        self.port = 8069
        # self.db = 'Liege_stock'
        # self.username = 'admin'
        # self.password = 'admin'
        # self.host = "localhost"
        # self.port = 9769
        self.odoo_connect = self.connect()
        self.file_path = argvs[2] # c'est le 2° paramètre défini dans le script qu'on appel : /home/exemple.csv ; (à savoir le /home/...)
        self.separator = argvs[3] # c'est le 3° paramètre défini dans le script qu'on appel : /home/exemple.csv ; (à savoir le ;)
        self.columns_mapping = [('id', 'PurchLineID'),
                                ('order_id', 'PurchID'),
                                ('display_name', 'ExternalitemID'),
                                ('product_qty', 'PurchQty'),
                                ('price_unit', 'PurchPrice'),
                                ('price_tax', 'PurchpriceVAT'),]

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
        # caratcères que nous ne pouvons pas accepter dans les celulles pour
        # l'export
        char_to_strip = "\n;"
        model_obj = self.odoo_connect.env[model_name]
        delay = date.today() - timedelta(days=200)
        delay = '{}'.format(delay)
        # TODO: Adapter le domaine de la méthode search pour synchroniser les
        #  bonne Pucharse order line (POL libérées et sans réponse de Dynamics
        object_ids = model_obj.browse(model_obj.search([('create_date','>=',delay),('dyn_liberer','=',False)]))
        lines = []
        lines.append([x[1] for x in self.columns_mapping])
        for obj in object_ids:
            row = []
            for col in self.columns_mapping:
                # la fonction strip enlève les carractères interdit dans les
                # cellules
                value = obj[col[0]]
                if hasattr(value, '_name'):
                    value = value.id
                if isinstance(value, basestring):
                    value = value.strip(char_to_strip)
                row.append(u'{}'.format(value))
            lines.append(row)
        return lines

    def write_odoo(self, model_name, dico):
        model_obj = self.odoo_connect.env[model_name]
        # for k, v in dico.iteritems():
        #     model_obj.import_from_dynamics([k], v)
        model_obj.import_from_dynamics(dico)


if __name__ == "__main__":
    try:
        argvs = sys.argv
        LOGGER.info(u"Script de synchro entre odoo/dynamics.\nparams: {argvs}"
                    .format(argvs=argvs))
        instance = CsvToOdooToCsv(argvs)
        action = argvs[1]
        if action == 'get':
            lines = instance.read_odoo('purchase.order.line')
            instance.write_csv(lines)
        if action == 'push':
            dico = instance.read_csv()
            instance.write_odoo('purchase.order.line', dico)
    except Exception, e:
        LOGGER.error(u"Script Error\nError info : {e}".format(e=e))
