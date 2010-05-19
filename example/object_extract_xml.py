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
from lxml.etree import tostring


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

group = OptionGroup(parser, 'Multi company default',
                "Application option")
group.add_option('-m', '--model', dest='model',
                default='res.partner',
                help='Enter the model name to check'),
#group.add_option('-c', '--company', dest='company',
#                default='',
#                help='Enter list of companies, seprate by a comma (,)')
group.add_option('-a', '--all', dest='all',
                action='store_true',
                default=False,
                help='Extract field if value is False, or blank')
group.add_option('', '--header', dest='header',
                action='store_true',
                default=False,
                help='Add XML and OpenObkect Header')
group.add_option('', '--indent', dest='indent',
                action='store_true',
                default=False,
                help='Indent the XML output')
parser.add_option_group(group)

opts, args = parser.parse_args()

try:
    cnx = Connection(server=opts.server, dbname=opts.dbname, login=opts.user,
                     password=opts.passwd)
except Exception, e:
    print '%s' % str(e)
    exit(1)

model = Object(cnx, opts.model)
model_data = Object(cnx, 'ir.model.data')

##
# Check if model exists and return all fields
#
try:
    fields = model.fields_get()
except Exception, e:
    print "Error object %s doesn't exists" % opts.model
    exit(2)


def Ir_Model_Data(model, id):
    """
    Search if the record was previously register in ir_model_data
    """
    args = [
        ('model','=', model),
        ('res_id', '=', id)
    ]
    ret = '%s_%d' % (model.replace('.','_'), id)
    res = model_data.search(args)
    if res:
        r = model_data.read(res, ['module','name'])[0]
        ret = '%s.%s' % (r['module'], r['name'])
    return ret

###
## Verify if there are records in the object
##
count = model.search_count([])
model_ids = model.search([], 0, count)

root = Element('openerp')
data = SubElement(root, 'data')

for m_id in model_ids:
    ##
    # Read the current id
    #
    mod = model.read(m_id)
    record = SubElement(data, 'record')
    record.set('model', opts.model)
    record.set('id', Ir_Model_Data(opts.model, m_id))
    for fld in fields:
        f_type = fields[fld]['type']
        if mod[fld] or opts.all:
            field = SubElement(record, 'field')
            field.set('name', fld)
            if f_type in('char','text'):
                field.text = mod[fld] or ''
            elif f_type in ('int','integer'):
                field.set('eval', mod[fld] and str(mod[fld]) or '0')
            elif f_type == 'float':
                field.set('eval', mod[fld] and str(mod[fld]) or '0.0')
            elif f_type == 'boolean':
                field.set('eval', str(mod[fld]) or 'False')
            elif f_type == 'date':
                if mod[fld]:
                    field.text = mod[fld]
                else:
                    field.set('eval', 'False')
            elif f_type == 'one2many':
                pass
            elif f_type == 'many2one':
                if mod[fld]:
                    field.set('ref', Ir_Model_Data(fields[fld]['relation'], mod[fld][0]))
                else:
                    field.set('eval', 'False')
            elif f_type == 'many2many':
                dd = ''
                for d in mod[fld]:
                    dd += "ref('%s')," % Ir_Model_Data(fields[fld]['relation'], d)
                if dd:
                    field.set('eval', '[(6,0,[%s])]' % dd[:-1])
                else:
                    field.set('eval', '[]')
            elif f_type == 'selection':
                if not mod[fld]:
                    field.set('eval', 'False')
                if isinstance(mod[fld], (int, float, bool)):
                    field.set('eval', str(mod[fld]))
                else:
                    field.text = str(mod[fld])
            else:
                field.text = str(mod[fld]) or ''

print tostring(root, encoding='UTF-8', xml_declaration=opts.header, pretty_print=opts.indent)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
