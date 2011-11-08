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
Export data to OpenOffice Sheet
"""

import sys
sys.path.append('../')

from oobjlib.connection import Connection
from oobjlib.component import Object
from oobjlib.common import GetParser
from optparse import OptionGroup
import os
import logging

__version__ = (0, 1)

parser = GetParser('Export data to OpenOffice Sheet', '.'.join(map(str, __version__)))
group = OptionGroup(parser, "Object arguments",
        "Application Options")
group.add_option('-f', '--file', dest='filename',
                 default=False,
                 help='Enter the name of the file to export')
group.add_option('-v', '--verbose', dest='verbose',
                 action='store_true',
                 default=False,
                 help='Add verbose mode')
group.add_option('-l', '--log-file', dest='logfile',
                 default=False,
                 help='Enter the name of the log file')
group.add_option('-m', '--model', dest='model',
                default=False,
                help='Enter the model name to export')
group.add_option('', '--language', dest='lang',
                 default='en_US',
                 help='Specify the language to search on translate field, default en_US')
group.add_option('-t', '--title', dest='title',
                 action='store_true',
                 default=False,
                 help='Write title header')
parser.add_option_group(group)

opts, args = parser.parse_args()

if opts.logfile:
    ch = logging.FileHandler(opts.logfile)
else:
    ch = logging.StreamHandler()

logger = logging.getLogger("export_ooo")
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
else:
    logger.error('Missing filename, abort!')
    sys.exit(2)

if not opts.model:
    logger.error('Misisng model to export, abort!')
    sys.exit(4)

logger.info('Language to import data: %s' % opts.lang)

try:
    logger.info('Open connection to "%s:%s" on "%s" with user "%s" ' % (opts.server, opts.port, opts.dbname, opts.user))
    cnx = Connection(
        server=opts.server,
        dbname=opts.dbname,
        login=opts.user,
        password=opts.passwd,
        port=opts.port)
except Exception, e:
    logger.error('Fail to connect to the server')
    logger.error('%s' % str(e))
    sys.exit(1)

model = Object(cnx, opts.model)

mod_count = model.search_count([])
logger.info('There are %d record to export' % mod_count)

fields = model.fields_get()
fields_name = fields.keys()

result = model.read(model.search([]))

from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TextProperties, ParagraphProperties, TableColumnProperties
from odf.text import P
from odf.table import Table, TableColumn, TableRow, TableCell

textdoc = OpenDocumentSpreadsheet()
tablecontents = Style(name="Table Contents", family="paragraph")
tablecontents.addElement(ParagraphProperties(numberlines="false", linenumber="0"))
tablecontents.addElement(TextProperties(fontweight="bold"))
textdoc.styles.addElement(tablecontents)

table = Table(name=opts.model)

if opts.title:
    logger.info('Write row header')
    tr = TableRow()
    table.addElement(tr)
    for f in fields_name:
        tc = TableCell(valuetype='string')
        tr.addElement(tc)
        p = P(stylename=tablecontents, text=unicode(fields[f]['string'], 'utf-8'))
        tc.addElement(p)

cpt = 0
for data in result:
    tr = TableRow()
    table.addElement(tr)
    for f in fields_name:
        logger.info('Extract line %d' % (cpt + 1))
        if cpt == (mod_count - 1):
            break

        d = result[cpt][f]
        f_type = fields[f]['type']

        if f_type == 'many2one':
            d = d and d[1] or ''
        elif f_type == 'many2many':
            d = ','.join(map(str, d))
        elif f_type == 'one2many':
            d = ','.join(map(str, d))

        if isinstance(d, int):
            tc = TableCell(valuetype="int", value=d)
        elif isinstance(d, float):
            tc = TableCell(valuetype="float", value=d)
        elif isinstance(d, bool):
            tc = TableCell(valuetype="bool", value=d)
        else:
            tc = TableCell(valuetype='string')

        tr.addElement(tc)
        if isinstance(d, unicode):
            p = P(stylename=tablecontents, text=d)
        else:
            p = P(stylename=tablecontents, text=unicode(str(d), 'utf-8'))
        tc.addElement(p)
    cpt += 1

textdoc.spreadsheet.addElement(table)
textdoc.save(opts.filename)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
