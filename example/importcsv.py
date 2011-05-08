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

parser = GetParser('Import CSV compatible with OpenERP', '0.2')
group = OptionGroup(parser, "Object arguments",
        "Application Options")
group.add_option('-f', '--file', dest='filename',
                 default=False,
                 help='Enter the name of the file to import')
group.add_option('','--directory', dest='directory',
                 default=False,
                 help='Indicate teh directory to scan file')
group.add_option('', '--separator', dest='separator',
                 default=',',
                 help='Enter the comma separator, default ","')
group.add_option('-v', '--verbose', dest='verbose',
                 action='store_true',
                 default=False,
                 help='Add verbose mode')
group.add_option('-l', '--log-file', dest='logfile',
                 default=False,
                 help='Enter the name of the log file')
group.add_option('-e', '--stop-on-error', dest='stop',
                 action='store_true',
                 default=False,
                 help='Stop treatment on error')
group.add_option('-t', '--transaction', dest='transaction',
                 action='store_true',
                 default=False,
                 help='Insert datas in one transaction')
group.add_option('', '--language', dest='lang',
                 default='en_US',
                 help='Specify the language to search on translate field, default en_US')
parser.add_option_group(group)

opts, args = parser.parse_args()

if opts.logfile:
    ch = logging.FileHandler(opts.logfile)
else:
    ch = logging.StreamHandler()

logger = logging.getLogger("importcsv")
if opts.verbose:
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
    ch.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

if opts.filename and opts.directory:
    logger.error('You cannot use --filename and --directory at the same time')
    sys.exit(1)

if opts.filename:
    opts.filename = os.path.expanduser(opts.filename)

if opts.directory:
    opts.directory = os.path.expanduser(opts.directory)

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


class StopError(Exception):
    pass


def execute_import(filename, connection, separator=',', transaction=False, error_stop=False):
    """
    Read the file, and launched import_data
    """
    model = filename.split('/').pop().replace('.csv', '')
    model = model[model.find('-') + 1:]
    logger.debug('model: %s' % model)

    obj = Object(connection, model)

    logger.info('Read and analyse the file content')
    fp = open(filename, 'r')
    header = False
    lines = []
    count = 0
    reader = csv.reader(fp, delimiter=separator)
    for line in reader:
        count += 1
        if not header:
            header = line
            logger.debug('header: %s' % str(header))
            continue

        lines.append(line)
        logger.debug('line: %s' %str(line))
    logger.info('Read the file content is finished')

    logger.info('Start import the content in OpenERP (%d datas)' % len(lines))
    count = 0
    ctx = {
        'defer_parent_store_computation': True,
        'lang': opts.lang,
    }
    if transaction:
        try:
            logger.info('Import %s lines in one transaction' % len(lines))
            res = obj.import_data(header, lines, 'init', '', False, ctx)
            if res[0] == -1:
                logger.error('%s' % res[2])
                logger.error('%s' % str(res[1]))
            logger.info('End transaction import')
        except Exception, e:
            logger.error(str(e))
            if error_stop:
                raise StopError(str(e))
    else:
        for l in lines:
            count += 1
            logger.debug('Import line %d :' % count)
            try:
                res = obj.import_data(header, [l], 'init', '', False, ctx)
                if res[0] == -1:
                    logger.error('%s' % res[2])
                    logger.error('%s' % str(res[1]))
            except Exception, e:
                logger.error(str(e))
                if error_stop:
                    raise StopError(str(e))
                break
    logger.info('Import finished')

if opts.filename:
    # Check if the file exists
    if not os.path.exists(opts.filename):
        logger.error("File %s seem doesn't exists" % opts.filename)
        sys.exit(2)

    # recherche du mon de l'objet dans le nom du fichier sans l'extension
    fn = opts.filename.split('/').pop()
    if not fn.endswith('.csv'):
        logger.error('File must have a CSV extension')
        sys.exit(4)
    logger.info('Start execute import on the selected file')
    execute_import(opts.filename, cnx, opts.separator, opts.transaction)

elif opts.directory:
    import glob
    list_file = glob.glob(os.path.join(opts.directory, '*.csv'))
    list_file.sort()
    for i in list_file:
        logger.info('Start execute import for %s' % i.split('/').pop())
        try:
            execute_import(i, cnx, opts.separator, opts.transaction)
        except StopError:
            if opts.stop:
                sys.exit(1)

else:
    logger.error('no specify --filename or --directory option')

logger.info('Import done')



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
