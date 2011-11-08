#!/usr/bin/env python
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
This script check all model in the module
and launch a search, read, field_view_get, etc...
"""

import sys
sys.path.append('../')

from oobjlib.connection import Connection
from oobjlib.component import Object
from oobjlib.common import GetParser
from optparse import OptionGroup


parser = GetParser('Regression model', '0.1')
group = OptionGroup(parser, 'Display information',
                "Others arguments")
group.add_option('--all-views', dest='all_views',
                action='store_true',
                default=False,
                help='Test all views, not only the default view'),
group.add_option('-q', '--quiet', dest='quiet',
                action='store_true',
                default=False,
                help='Reduce output only with error'),
group.add_option('-o', '--openerp-version', dest='oerp_version',
                default=6,
                help='Indicate the version of OpenERP (5 or 6)')
parser.add_option_group(group)
opts, args = parser.parse_args()

try:
    cnx = Connection(
        server=opts.server,
        dbname=opts.dbname,
        login=opts.user,
        password=opts.passwd,
        port=opts.port)
except Exception, e:
    print '%s' % str(e)
    sys.exit(1)

mod = Object(cnx, 'ir.model')

if opts.oerp_version == '5':
    print 'version 5'
    model = mod.search([])
else:
    print 'version 6'
    model = mod.search([('osv_memory', '=', False)])


print 80 * '-'
print '| Model                                         | Search |  Read  | View XML |'
print 80 * '-'

footer = '--- FOOTER REPORT ---\n'

for m in mod.read(model):
    if m['model'].startswith('ir_') or m['model'].find('wizard') >= 0:
        continue

    t = Object(cnx, m['model'])
    try:
        t_ids = t.search([])
        search = ('%d' % len(t_ids)).zfill(4)
    except Exception, e:
        search = 'ERR'
        footer += 'Objet: %s\n' % m['model']
        footer += 'Message: %s\n' % str(e)
    try:
        read = 'NA '
        if t_ids:
            end_id = min(10, len(t_ids)) - 1
            tr = t.read(t_ids[0:end_id])
            read = 'OK '
    except Exception, e:
        read = 'ERR'   #'ERR'
        footer += 'Objet: %s\n' % m['model']
        footer += 'Message: %s\n' % str(e)

    try:
        a = t.fields_view_get()
        if opts.all_views:
            v = Object(cnx, 'ir.ui.view')
            v_ids = v.search([('model', '=', m['model'])])
            v_data = v.read(v_ids, ['type'])
            for data in v_data:
                a = t.fields_view_get(data['id'], data['type'])
        view = 'OK '
    except Exception, e:
        view = 'ERR'
        footer += 'Objet: %s\n' % m['model']
        footer += 'Message: %s\n' % str(e)

    if opts.quiet:
        if (search == 'ERR' or read == 'ERR' or view == 'ERR'):
            print '| %s | %s   | %s    | %s   |' % (m['model'].ljust(45), search, read, view)
    else:
        print '| %s | %s   | %s    | %s   |' % (m['model'].ljust(45), search, read, view)

print 80 * '*'
print footer

if (search == 'ERR' or read == 'ERR' or view == 'ERR'):
    sys.exit(2)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
