# --*- coding: utf-8 -*-
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
Common.py containt common information from all test files
"""

from optparse import OptionParser

def GetParser(appname, version):
    """Creates and returns the commmand line parser"""
    usage = "Usage: %prog [options]"
    parser = OptionParser(usage, prog=appname,
                          version=version)
    parser.add_option('-s', '--server', dest='server',
                      default='localhost',
                      help='Indicate the server name or IP (default: localhost)')
    parser.add_option('-p', '--port', dest='port',
                      default=8069,
                      help='Port (default: 8069)')
    parser.add_option('-d', '--dbname', dest='dbname',
                      default='demo',
                      help='Name of the database (default: demo)')
    parser.add_option('-u', '--user', dest='user',
                      default='admin',
                      help='Select an OpenERP User (default: admin)')
    parser.add_option('-w', '--password', dest='passwd',
                      default='admin',
                      help='Enter the user password (default: admin)')
    parser.add_option('-a', '--admin', dest='admin',
                      default='admin',
                      help='Default admin serveur, use for create/backup/restore database (default: admin)')

    return parser

class UniqueList(list):
    """Inhherit list to be unique"""
    def append(self, o):
        if o and o not in self:
            super(unique_list, self).append(o)

    def insert(self, p, o):
        if o and o not in self:
            super(unique_list, self).insert(p, o)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
