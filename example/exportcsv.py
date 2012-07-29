#!/usr/bin/env python
# --*- coding: utf-8 -*-
##############################################################################
#
#    OpenObject Library
#    Copyright (C) 2009-2011 Syleam (<http://syleam.fr>). Christophe Chauvet
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
This script check all model in the module
and launch a search, read, field_view_get, etc...
"""

import sys
sys.path.append('../')

from oobjlib.connection import Connection
from oobjlib.component import Object
from oobjlib.common import GetParser
from optparse import OptionGroup
import os
import logging
import csv

parser = GetParser('Export CSV compatible with OpenERP', '0.2')
group = OptionGroup(parser, "Object arguments", "Application Options")
group.add_option('-f', '--file', dest='filename', default=False, help='Enter the name of the file to export')
group.add_option('-m', '--model', dest='model', default=False, help='Enter the name of the model to export')
group.add_option('', '--ids', dest='ids', default=False, help='Enter the ids to export')
group.add_option('', '--fields', dest='fields', default=False, help='Enter the name of the fields to export')
group.add_option('', '--separator', dest='separator', default=',', help='Enter the comma separator, default ","')
group.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Add verbose mode')
group.add_option('-l', '--log-file', dest='logfile', default=False, help='Enter the name of the log file')
group.add_option('', '--language', dest='lang', default='en_US', help='Specify the language to search on translate field, default en_US')
group.add_option('', '--with-inactive', dest='inactive', action='store_true', default=False, help='Extract inactive records')
parser.add_option_group(group)

opts, args = parser.parse_args()

if opts.logfile:
    ch = logging.FileHandler(opts.logfile)
else:
    ch = logging.StreamHandler()

logger = logging.getLogger("exportcsv")
if opts.verbose:
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
    ch.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

if opts.filename:
    opts.filename = os.path.expanduser(opts.filename)

logger.info('Language to export data: %s' % opts.lang)

try:
    logger.info('Open connection to "%s:%s" on "%s" with user "%s" ' % (opts.server, opts.port, opts.dbname, opts.user))
    cnx = Connection(
        server=opts.server,
        dbname=opts.dbname,
        login=opts.user,
        password=opts.passwd,
        port=opts.port,
    )
except Exception, e:
    logger.error('Fail to connect to the server')
    logger.error('%s' % str(e))
    sys.exit(1)


class StopError(Exception):
    pass


filename = opts.filename
if not opts.filename:
    filename = '%s.csv' % opts.model

# recherche du mon de l'objet dans le nom du fichier sans l'extension
obj = Object(cnx, opts.model)

ctx = {'lang': opts.lang}
if opts.inactive:
    ctx['active_test'] = False

if not opts.ids:
    # Get all ids
    ids = obj.search([])
else:
    ids = [int(x.strip()) for x in opts.ids.split(',')]

if not opts.fields:
    # get all fields
    fields = obj.fields_get_keys()
else:
    fields = opts.fields.split(',')

logger.info('Start execute export on the selected file')
result = obj.export_data(ids, fields, ctx)['datas']

csvWriter = csv.writer(file(filename, 'wb+'), delimiter=opts.separator, quoting=csv.QUOTE_NONNUMERIC)
csvWriter.writerow(fields)

for data in result:
    row = []
    for d in data:
        if isinstance(d, basestring):
            d = d.replace('\n',' ').replace('\t',' ')
            try:
                d = d.encode('utf-8')
            except:
                pass
        if d is False: d = None
        row.append(d)

    csvWriter.writerow(row)

logger.info('Export done')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
