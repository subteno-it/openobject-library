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

import xmlrpclib
from socket import error as socket_error

class Connection(object):
    """Create a new database connection"""
    def __init__(self, server="localhost", port=8069, dbname="terp", login=None, password=None):
        self.server, self.port = server, int(port)
        self._url = "http://%s:%d/xmlrpc/common" % (self.server, self.port)
        self._sock = xmlrpclib.ServerProxy(self._url)
        self.dbname = dbname
        self.login, self.password = login, password

        try:
            self.userid = self._sock.login(dbname, login, password)
        except socket_error, se:
            raise Exception('Unable to connect to http://%s:%d: %s' % (self.server, self.port, se.args[1]))
        except xmlrpclib.Fault, err:
            raise Exception('%s: %s' % (err.faultCode.encode('utf-8'), err.faultString.encode('utf-8')))
        if not self.userid:
            raise Exception("Unable to connect to database %s using %s" % (dbname, login,))

    def __str__(self):
        return '%s [%s]' % (self._url, self.dbname)

class Database(object):
    """Instanciate Database Object"""
    def __init__(self, server="localhost", port=8069, supadminpass='admin'):
        self.supadminpass = supadminpass
        self.server, self.port = server, int(port)
        self._url = "http://%s:%d/xmlrpc/db" % (self.server, self.port)
        self._sock = xmlrpclib.ServerProxy(self._url)

    def __getattr__(self, name):
        def proxy(*args, **kwargs):
            return getattr(self._sock, name)(self.supadminpass, *args, **kwargs)
        return proxy

    def list(self):
        """Return the list of database"""
        return self._sock.list()

    def __str__(self):
        """representation of this object"""
        return '%s [%s]' % (self._url, self.supadminpass)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
