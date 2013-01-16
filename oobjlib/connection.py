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

import netrpclib


class OobjBase(object):
    __slots__ = ('server', 'port', '_sock', 'server_version')

    def __init__(self, server='localhost', port=8070):
        self.server = server
        self.port = int(port)
        self._sock = netrpclib.NetrpcSocket(self.server, self.port)
        # Workaround for connection errors, waiting for a better solution
        self.server_version = self._sock.db('server_version').split('.')
        if self.server_version[0] <= '5':
            self._sock.disconnect()
            self._sock = netrpclib.NetrpcSocket(self.server, self.port, reconnect=True)


class Connection(OobjBase):
    """Create a new database connection"""
    __slots__ = ('dbname', 'login', 'password', 'userid', 'context')

    def __init__(self, server='localhost', port=8070, dbname='demo', login=None, password=None):
        super(Connection, self).__init__(server=server, port=port)
        self.dbname = dbname
        self.login = login
        self.password = password

        # Login on the database
        self.userid = self._sock.common('login', dbname, login, password)
        # Retrieve context for this user
        self.context = self._sock.object('execute', self.dbname, self.userid, self.password, 'res.users', 'context_get')

    def __str__(self):
        """
        Human readable representation of this object
        """
        return '%s <%s@%s:%d [%s]>' % (self.__class__.__name__, self.login, self.server, self.port, self.dbname)

    def __repr__(self):
        """
        Pythonic representation of this object
        """
        return "oobjlib.connection.%s('%s', %d, '%s', '%s', '%s')" % (self.__class__.__name__, self.server, self.port, self.dbname, self.login, self.password)


class Database(OobjBase):
    """Instanciate Database Object"""
    __slots__ = ('supadminpass')

    def __init__(self, server='localhost', port=8170, supadminpass='admin'):
        super(Database, self).__init__(server=server, port=port)
        self.supadminpass = supadminpass

    def __getattr__(self, name):
        """
        Forward all method calls to the socket
        """
        return lambda *args, **kwargs: self._sock.db(name, self.supadminpass, *args, **kwargs)

    def __str__(self):
        """
        Human readable representation of this object
        """
        return '%s <%s:%d [%s]>' % (self.__class__.__name__, self.server, self.port, self.supadminpass)

    def __repr__(self):
        """
        Pythonic representation of this object
        """
        return "oobjlib.connection.%s('%s', %d, '%s')" % (self.__class__.__name__, self.server, self.port, self.supadminpass)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
