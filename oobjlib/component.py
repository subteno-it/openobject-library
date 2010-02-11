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

import xmlrpclib
from socket import error as socket_error

# TODO abstract the use of the context

class Object(object):
    """
    Create an Object relate to an OpenObject model
    """
    def __init__(self, connection, model):
        self._connection = connection
        self._model = model
        self._url = "http://%s:%d/xmlrpc/object" % (connection.server, connection.port)
        self._sock = xmlrpclib.ServerProxy(self._url)

    def __getattr__(self, name):
        def proxy(*args, **kwargs):
            try:
                return self._sock.execute(self._connection.dbname, self._connection.userid, self._connection.password, self._model, name, *args, **kwargs)
            except socket_error, se:
                raise Exception('Unable to connect to http://%s:%d: %s' % (server, port, se.args[1]))
            except xmlrpclib.Fault, err:
                raise Exception('%r: %s' % (err.faultCode, err.faultString.encode('utf-8')))
        return proxy

    def select(self, domain = None, fields=None):
        ids = self.search(domain or [])
        return self.read(ids, fields or [])

    def __str__(self,):
        return '%s [%s]' % (self._url, self._model)

class Wizard(object):
    """
    Manage a Wizard by pass a value and execute one of these actions
    """
    def __init__(self, connection, name):
        self._connection = connection
        self._name = name
        u = "http://%s:%d/xmlrpc/wizard" % (connection.server, connection.port)
        self._sock = xmlrpclib.ServerProxy(u)
        try:
            self._id = self._sock.create(self._connection.dbname,
                                         self._connection.userid,
                                         self._connection.password,
                                         self._name)
        except socket_error, se:
            raise Exception('Unable to connect to http://%s:%d: %s' % (server, port, se.args[1]))
        except xmlrpclib.Fault, err:
            raise Exception('%r: %s' % (err.faultCode, err.faultString.encode('utf-8')))

    def __getattr__(self, state):
        def proxy(**kwargs):
            try:
                return self._sock.execute(self._connection.dbname,
                                          self._connection.userid,
                                          self._connection.password,
                                          self._id, kwargs, state)
            except socket_error, se:
                raise Exception('Unable to connect to http://%s:%d: %s' % (server, port, se.args[1]))
            except xmlrpclib.Fault, err:
                raise Exception('%r: %s' % (err.faultCode, err.faultString.encode('utf-8')))
        return proxy

class Workflow(object):
    """
    Manage workflow
    """
    def __init__(self, connection, model):
        self._connection = connection
        self._model = model
        u = "http://%s:%d/xmlrpc/object" % (connection.server, connection.port)
        self._sock = xmlrpclib.ServerProxy(u)

    def __getattr__(self, name):
        def proxy(oid):
            try:
                return self._sock.exec_workflow(self._connection.dbname,
                                            self._connection.userid,
                                            self._connection.password,
                                            self._model, name, oid)
            except socket_error, se:
                raise Exception('Unable to connect to http://%s:%d: %s' % (server, port, se.args[1]))
            except xmlrpclib.Fault, err:
                raise Exception('%r: %s' % (err.faultCode, err.faultString.encode('utf-8')))
        return proxy


def demo():
    db = Database()
    print repr(db.list())

    cnx = Connection(dbname="demo", login="admin", password="admin")
    modules = Object(cnx, "ir.module.module")

    ids = modules.search([('state', '=', 'installed')])
    for p in modules.read(ids, ['name']):
        print p['name']

if __name__ == '__main__':
    demo()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
