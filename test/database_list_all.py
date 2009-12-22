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
Connect to the server and return the list of databases
"""

import sys
sys.path.append('../')

from oobjlib.connection import Database

from common import GetParser

parser = GetParser('Database List', '0.1')
opts, args = parser.parse_args()

try:
    db = Database(
        server=opts.server,
        port=opts.port,
        supadminpass=opts.admin)
except Exception, e:
    print '%s' % str(e)
    exit(1)

print '--[Server Connection]-i---------------------'
print '%s' % str(db)

print '--[Database list]---------------------------'
for d in  db.list():
    print '* %s' % d

print '--[End]-------------------------------------'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
