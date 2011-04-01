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
This program check if parent_store on object is correct, if not
you must correct it
"""

import sys
sys.path.append('../')

from oobjlib.connection import Connection
from oobjlib.component import Object
from oobjlib.common import GetParser
from optparse import OptionGroup

import logging

parser = GetParser('Check parent store', '0.1')
group = OptionGroup(parser, "Object arguments",
        "Application Options")
group.add_option('-m', '--model', dest='model',
                 default=False,
                 help='Enter the name of the file to import')
group.add_option('-f','--field', dest='field',
                 default='parent_id',
                 help='Indicate the parent field (default parent_id)')
group.add_option('-v', '--verbose', dest='verbose',
                 action='store_true',
                 default=False,
                 help='Add verbose mode')
group.add_option('', '--fix', dest='fix',
                 action='store_true',
                 default=False,
                 help='If error found on parent store, we fix it')
parser.add_option_group(group)

opts, args = parser.parse_args()

logger = logging.getLogger("importcsv")
ch = logging.StreamHandler()
if opts.verbose:
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
    ch.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.info('Model: %s' % (opts.model,))
logger.info('Field: %s' % (opts.field,))

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
model_ids = model.search([])
model_lists = model.read(model_ids, [opts.field,'parent_left','parent_right'])
models = dict(map(lambda x: (x['id'],x), model_lists))
try:
    for a in model_lists:
        logger.debug('id: %d' % a['id'])
        if a[opts.field]:
            assert a['parent_left'] > models[a[opts.field][0]]['parent_left'], '%s > %s' % (a['parent_left'], models[a[opts.field][0]]['parent_left'])
            assert a['parent_right'] < models[a[opts.field][0]]['parent_right'], '%s > %s' % (a['parent_right'], models[a[opts.field][0]]['parent_right'])
        assert a['parent_left'] < a['parent_right']
        for a2 in model_lists:
            assert not ((a2['parent_right']>a['parent_left']) and 
                (a2['parent_left']<a['parent_left']) and 
                (a2['parent_right']<a['parent_right']))
            if a2[opts.field]==a['id']:
                assert (a2['parent_left']>a['parent_left']) and (a2['parent_right']<a['parent_right'])
except AssertionError, e:
    logger.error('Fail: %s' % str(e))
    if opts.fix:
        logger.info('Begin to fix the problem')
        model._parent_store_compute()
        logger.info('End fix')

logger.info('Check End and complete')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
