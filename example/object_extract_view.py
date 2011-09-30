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
Extract XML for selected object or the globality
"""

import sys
sys.path.append('../')

from oobjlib.connection import Connection
from oobjlib.component import Object
from optparse import OptionParser, OptionGroup
from lxml.etree import Element, SubElement
from lxml.etree import tostring, fromstring


usage = "Usage %prog [options]"
__version__ = '1.0'

parser = OptionParser(usage, prog='object_extract_xml.py',
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

group = OptionGroup(parser, 'View parameter',
                "Application option")
group.add_option('', '--id', dest='id', type=int,
                 default=False,
                 help='Indicate which ID you want to extract')
parser.add_option_group(group)

opts, args = parser.parse_args()

try:
    cnx = Connection(server=opts.server, dbname=opts.dbname, login=opts.user,
                     password=opts.passwd, port=opts.port)
except Exception, e:
    print '%s' % str(e)
    exit(1)

if not opts.id:
    print '--id argument is required!'
    exit(1)

model_view = Object(cnx, 'ir.ui.view')
model_data = Object(cnx, 'ir.model.data')

def Ir_Model_Data(model, id):
    """
    Search if the record was previously register in ir_model_data
    """
    args = [
        ('model', '=', model),
        ('res_id', '=', id)
    ]
    ret = '%s_%d' % (model.replace('.', '_'), id)
    res = model_data.search(args)
    if res:
        r = model_data.read(res, ['module', 'name'])[0]
        ret = '%s.%s' % (r['module'], r['name'])
    return ret

root = Element('record')
root.set('model','ir.ui.view')
root.set('id', Ir_Model_Data('ir.ui.view', opts.id))

view = model_view.read(opts.id)

for f in ['name','model','type','priority','inherit_id','arch']:
    if f == 'inherit_id' and not view[f]:
        continue

    field = SubElement(root ,'field')
    if f == 'inherit_id':
        field.set('name', f)
        field.set('ref', Ir_Model_Data('ir.ui.view', view[f][0]))
    elif f == 'arch':
        field.set('name', f)
        field.set('type', 'xml')
        tmp_arch = fromstring(view[f])
        field.append(tmp_arch)
    else:
        field.set('name', f)
        field.text = str(view[f]).encode('utf-8')


print tostring(root, encoding='UTF-8', xml_declaration=False, pretty_print=True)
