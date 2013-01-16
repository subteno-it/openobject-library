# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenObject Library
#    Copyright (C) 2009 Tiny (<http://tiny.be>). Christophe Simonis
#                  All Rights Reserved
#    Copyright (C) 2009 Syleam (<http://syleam.fr>). Christophe Chauvet
#                  All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""
This module is compose by component available in OpenObject
"""

import time
import base64
import tempfile


class OObjlibException(Exception):
    pass


class Object(object):
    """
    Create an Object relate to an OpenObject model
    """
    def __init__(self, connection, model):
        self._connection = connection
        self._model = model

    def __getattr__(self, name):
        """
        Forward all method calls to the socket
        """
        return lambda *args, **kwargs: self._connection._sock.object('execute', self._connection.dbname, self._connection.userid, self._connection.password, self._model, name, *args, **kwargs)

    def select(self, domain=None, fields=None):
        ids = self.search(domain or [])
        return self.read(ids, fields or [])

    def __str__(self,):
        return "%s '%s' <%s@%s:%d [%s]>" % (self.__class__.__name__, self._model, self._connection.login, self._connection.server, self._connection.port, self._connection.dbname)


class Wizard(object):
    """
    Manage a Wizard by pass a value and execute one of these actions
    """
    def __init__(self, connection, name):
        self._connection = connection
        self._name = name
        self._id = self._connection._sock.wizard('create', self._connection.dbname, self._connection.userid, self._connection.password, self._name)

    def __getattr__(self, state):
        return lambda *args, **kwargs: self._connection._sock.wizard('execute', self._connection.dbname, self._connection.userid, self._connection.password, self._id, kwargs, state)


class Workflow(object):
    """
    Manage workflow
    """
    def __init__(self, connection, model):
        self._connection = connection
        self._model = model

    def __getattr__(self, name):
        return lambda oid: self._connection._sock.object('exec_workflow', self._connection.dbname, self._connection.userid, self._connection.password, self._model, name, oid)


class Report(object):
    """
    Execute de report and retrieve it as attchament
    """
    def __init__(self, connection, model, report_name):
        """
        :param connection: Instance of the Connection object
        :param model: name of the model for the report
        :param report_name: name of the registered report
        """
        self._connection = connection
        self._report_name = report_name
        self._model = model

    def retrieve(self, ids):
        """
        Execute the report and retrieve it
        """
        id_report = self._connection._sock.report('report', self._connection.dbname, self._connection.userid, self._connection.password, self._report_name, ids, {
            'model': self._model, 'id': ids[0], 'report_type': 'pdf'
        }, self._connection.context)

        time.sleep(5)
        state = False
        attempt = 0

        while not state:
            report = self._connection._sock.report('report_get', self._connection.dbname, self._connection.userid, self._connection.password, id_report)
            state = report['state']
            if not state:
                time.sleep(1)
            attempt += 1
            if attempt > 200:
                raise OObjlibException('Printing aborted, too long delay !')

        filename = tempfile.mkstemp(prefix='oobjlib-', suffix='-report.pdf')
        string_pdf = base64.decodestring(report['result'])
        file_pdf = open(filename[1], 'w')
        file_pdf.write(string_pdf)
        file_pdf.close()

        return filename[1]


def demo():
    from connection import Connection, Database
    db = Database()
    print repr(db.list())

    cnx = Connection(dbname='demo', login='admin', password='admin')
    modules = Object(cnx, 'ir.module.module')

    ids = modules.search([('state', '=', 'installed')])
    for p in modules.read(ids, ['name']):
        print p['name']

if __name__ == '__main__':
    demo()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
