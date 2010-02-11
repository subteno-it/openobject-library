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
from oobjlib.component import Workflow
from oobjlib.common import GetParser
from optparse import OptionGroup

parser = GetParser('Workflow manager', '0.1')

common = OptionGroup(parser, "Application",
        "Application option")
common.add_option('-m','--model', dest='model',
                 default='res.partner',
                 help='select the model')
common.add_option('', '--id', dest='id',
                 default=0,
                 help='Enter the id of record')
parser.add_option_group(common)

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
    exit(1)

acc = Workflow(cnx, opts.model)

try:
    acc.invoice_open(int(opts.id))
except Exception, err:
    print '%r' % err


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
