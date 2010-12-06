# --*- coding: utf-8 -*-
##############################################################################
#
#    OpenObject Library
#    Copyright (C) 2009-2010 Syleam (<http://syleam.fr>). Christophe Chauvet
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
NETRPC Library, Netrpc is more faster than xmlrpc
This implementation is based on xmlrpclib
"""
from socket import socket
from socket import AF_INET, SOCK_STREAM, SHUT_RDWR
from cPickle import dumps, loads
import sys


class Fault(Exception):
    """
    Define an exception that can be used with

    try
        ....
    except netrpclib.Fault, err:
        print '%s :: %s' % (err.faultCode, err.faultString)
    """
    def __init__(self, eCode, eString):
        self.faultCode = eCode
        self.faultString = eString
        self.args = (eCode, eString)


class NetrpcSocket:
    """
    NETRPC Socket
    """
    __slots__ = ('sock')

    def __init__(self, sock=None, timeout=120):
        if sock is None:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = sock
        self.sock.settimeout(timeout)

    def connect(self, host, port=False):
        if not port:
            protocol, buf = host.split('//')
            host, port = buf.split(':')
        self.sock.connect((host, int(port)))

    def disconnect(self):
        # on Mac, the connection is automatically shutdown when the server disconnect.
        # see http://bugs.python.org/issue4397
        if sys.platform != 'darwin':
            self.sock.shutdown(SHUT_RDWR)
        self.sock.close()

    def send(self, msg, exception=False, traceback=None):
        msg = dumps([msg, traceback])
        self.sock.sendall('%8d%s%s' % (len(msg), exception and "1" or "0", msg))

    def recv(self):
        def read(socket, size):
            buf = ''
            while len(buf) < size:
                chunk = self.sock.recv(size - len(buf))
                if chunk == '':
                    raise RuntimeError('socket connection broken')
                buf += chunk
            return buf

        size = int(read(self.sock, 8))
        buf = read(self.sock, 1)
        exception = buf != '0' and buf or False
        res = loads(read(self.sock, size))

        if isinstance(res[0], Exception):
            if exception:
                raise Fault(str(res[-2]), str(res[1]))
            raise res[0]
        else:
            return res[0]

if __name__ == '__main__':
    def message(title='', traceback=None):
        res = '---[ %s ]' % title
        res = res + ((80 - len(res)) * '-')
        if traceback is None:
            res += ' (OK)'
        else:
            res += ' (FAIL)'
            res += '\n%s' % traceback
        print res

    net = NetrpcSocket()
    net.connect('localhost', 8070)
    net.send(('db', 'list'))
    res = net.recv()
    net.disconnect()
    try:
        assert type(res) == type([]), 'result is not a list []'
        message('List all databases')
    except AssertionError, e:
        message('List all databases', e.message)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
