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
Extract XML for properties terms, to copy/paste in iReport
"""

import sys
sys.path.append('../')

from oobjlib.connection import Connection
from oobjlib.component import Object
from optparse import OptionParser, OptionGroup
from lxml.etree import Element, SubElement, CDATA
from lxml.etree import tostring


usage = "Usage %prog [options]"
__version__ = '1.0'

parser = OptionParser(usage, prog='Jasper Export Terms',
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
group.add_option('', '--service', dest='service',
                 default=False,
                 help='Indicate which service name, you want to extract')
parser.add_option_group(group)

opts, args = parser.parse_args()

try:
    cnx = Connection(server=opts.server, dbname=opts.dbname, login=opts.user,
                     password=opts.passwd, port=opts.port)
except Exception, e:
    print '%s' % str(e)
    exit(1)

if not opts.service:
    print '--service argument is required!'
    exit(1)

jasper_obj = Object(cnx, 'jasper.document')
label_obj = Object(cnx, 'jasper.document.label')

root = Element('jasperReport', {'name': 'to_be_defined', 'language': 'groovy', 'pageWidth': '595',
                                'pageHeight': '842', 'columnWidth': '555', 'leftMargin': '20',
                                'rightMargin': '20', 'topMargin': '20', 'bottomMargin': '20'})
#root.set('name', 'to_be_defined')
#root.set('language', 'groovy')
#root.set('pageWidth', '595')
#root.set('pageHeight', '842')
#root.set('columnWidth', '555')
#root.set('leftMargin', '20')
#root.set('rightMargin', '20')
#root.set('topMargin', '20')
#root.set('bottomMargin', '20')

jasper_ids = jasper_obj.search([('service','=',opts.service)])
if not jasper_ids:
    print 'Service %s not found' % opts.service
    exit(1)

jasper = jasper_obj.read(jasper_ids[0])

if isinstance(jasper, list):
    jasper = jasper[0]

#print jasper

for lab in label_obj.read(jasper['label_ids'], ['name','value']):
    #print lab

    #<parameter name="I18N_TITLE" class="java.lang.String" isForPrompting="false">
    #        <defaultValueExpression><![CDATA["BON DE RETOUR S.A.V."]]></defaultValueExpression>
    #</parameter>
    parameter = SubElement(root, 'parameter')
    parameter.set('name', 'I18N_' + lab['name'].upper())
    parameter.set('class', 'java.lang.String')
    parameter.set('isForPrompting', 'false')
    defaultvalue = SubElement(parameter, 'defaultValueExpression')
    defaultvalue.text = CDATA('"' + lab['value'] + '"')

print tostring(root, encoding='UTF-8', xml_declaration=False, pretty_print=True)
