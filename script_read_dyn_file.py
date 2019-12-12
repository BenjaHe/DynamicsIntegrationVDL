# /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import sys

import odoorpc

_logger = logging.getLogger(__name__)


class CsvToOdoo(object):
    def __init__(self, argvs):
        self.argvs = argvs
        # notice: parent class was like that: "parenet_class.ClassName2"
        self.db = 'copie_prod_13nov2019'
        self.username = 'admin'
        self.password = 'taivoN78'
        self.host = "192.168.232.47"
        self.port = 8069
        self.odoo_connect = self.connect()
        self.file_path = argvs[1] # c'est le 1° paramètre défini dans le script qu'on appel : /home/exemple.csv ; (à savoir le /home/...)
        self.separator = argvs[2] # c'est le 2° paramètre défini dans le script qu'on appel : /home/exemple.csv ; (à savoir le ;)

    def connect(self):
        odoo = odoorpc.ODOO(host=self.host, port=self.port)
        odoo.login(self.db, self.username, self.password)
        return odoo

    def read_csv(self):
        f = open(self.file_path, 'r') # 'r' pour dire qu'on se met en read sur le fichier
        lines = f.readlines()
        line_nbr = 0 # on définit la ligne 0 pour ensuite dire qu'on va commencer à lire la ligne 1 (car entête en ligne 0).
        dico = {} # on défini un dictionnaire de données.
        for r in lines: # r = row
            if line_nbr == 0:
                line_nbr += 1
                continue
            r = r.split(self.separator) # on passe de colonne quand on passe sur le ;
            id = int(r[0]) # on défini la première variable du dico => r[0] : chaque row, colonne 1
            name = r[2] # 2° colonne avec le nom du comptable (qui sera un one2may).
            state = r[2].rstrip() # idem mais .rstrip pour gérer \n pour dire qu'on arrive en bout de ligne et qu'il faut faire un saut de ligne
            dico[id] = {'name':name,'dyn_state': state} # la première colonne est utilisée comme id du dictionnaire et les autres colonnes sont mises dans {}
            # donc si on a 3 colonnes : dico[id] = {'dyn_state': state, 'nom de le colonne':nom de la variable}
            line_nbr += 1
        return dico

    def write(self, model_name, dico):
        model_obj = self.odoo_connect.env[model_name]
        for k,v in dico.iteritems():
            model_obj.write([k], v)


if __name__ == "__main__":
    argvs = sys.argv
    instance = CsvToOdoo(argvs)
    dico = instance.read_csv()
    instance.write('purchase.order.line', dico)