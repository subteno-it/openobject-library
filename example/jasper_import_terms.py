#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenObject Library
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
Import CSV file for labels terms
"""

import sys
sys.path.append('../')

from oobjlib.connection import Connection
from oobjlib.component import Object
from optparse import OptionParser, OptionGroup
import csv


usage = "Usage %prog [options]"
__version__ = '1.0'

parser = OptionParser(usage, prog='Jasper Import Terms',
        version=__version__)
common = OptionGroup(parser, "Common option",
                "OpenERP specific option")
common.add_option('-s', '--server', dest='server',
                  default='localhost',
                  help='Indicate the server name or IP (default: localhost)')
common.add_option('-p', '--port', dest='port',
                  default=8069,
                  help='Port (default: 8069)')
common.add_option('-d', '--dbname', dest='dbname',
                  default='demo',
                  help='Name of the database (default: demo)')
common.add_option('-u', '--user', dest='user',
                  default='admin',
                  help='Select an OpenERP User (default: admin)')
common.add_option('-w', '--password', dest='passwd',
                  default='admin',
                  help='Enter the user password (default: admin)')
parser.add_option_group(common)

group = OptionGroup(parser, 'Jasper Document',
                "Application option")
group.add_option('', '--file', dest='filename',
                 default=False,
                 help='Indicate the filename to import')
parser.add_option_group(group)

opts, args = parser.parse_args()

try:
    cnx = Connection(server=opts.server, dbname=opts.dbname, login=opts.user,
                     password=opts.passwd, port=opts.port)
except Exception, e:
    print '%s' % str(e)
    exit(1)

if not opts.filename:
    print '--file argument is required!'
    exit(1)

jasper_obj = Object(cnx, 'jasper.document')
label_obj = Object(cnx, 'jasper.document.label')


fp = open(opts.filename, 'r')
reader = csv.DictReader(fp, delimiter=',')

service_cache = {}

def format_code(code):
    code = code.upper()
    code = code.replace(' ', '_')
    return code

for l in reader:
    #print l
    if l['service'] in service_cache:
        jasper_id = service_cache[l['service']]
    else:
        jasper_ids = jasper_obj.search([('service', '=', l['service'])])
        if not jasper_ids:
            print 'Service %s not found' % opts.service
            exit(1)
        jasper_id = jasper_ids[0]
        service_cache[l['service']] = jasper_id

    #search if label already exists
    lab_ids = label_obj.search([('document_id', '=', jasper_id), ('name', '=', format_code(l['code']))])
    if lab_ids:
        #we update it
        label_obj.write([lab_ids[0]], {'value': l['message']})
        print 'UPDATE: %s -> %s' % (format_code(l['code']), l['message'])
    else:
        # we create it
        label_obj.create({'document_id': jasper_id, 'name': format_code(l['code']), 'value': l['message']})
        print 'CREATE: %s -> %s' % (format_code(l['code']), l['message'])

