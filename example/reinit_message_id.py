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
Fix all history message with message ID (RFC822)
"""

import sys
sys.path.append('../')

from oobjlib.connection import Connection
from oobjlib.component import Object
from optparse import OptionParser, OptionGroup

import hashlib
import time

usage = "Usage %prog [options]"
__version__ = '1.0'

parser = OptionParser(usage, prog='object_check_rules.py',
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
                  default='demo',
                  help='Select an OpenERP User (default: demo)')
common.add_option('-w', '--password', dest='passwd',
                  default='demo',
                  help='Enter the user password (default: demo)')
parser.add_option_group(common)

group = OptionGroup(parser, 'Multi company default',
                "Application option")
group.add_option('-m', '--model', dest='model',
                default='res.partner',
                help='Enter the model name to check'),
group.add_option('-l', '--legend', dest='legend',
                action="store_true",
                default=False,
                help='List the company by name and their ID')
parser.add_option_group(group)

opts, args = parser.parse_args()

try:
    cnx = Connection(server=opts.server, dbname=opts.dbname, login=opts.user, port=opts.port,
                     password=opts.passwd)
except Exception, e:
    print '%s' % str(e)
    exit(1)


def generate_tracking_message_id(openobject_id):
    """Returns a string that can be used in the Message-ID RFC822 header field so we
       can track the replies related to a given object thanks to the "In-Reply-To" or
       "References" fields that Mail User Agents will set.
    """
    s = hashlib.sha1()
    s.update(str(time.time()))
    return "<%s-openobject-%s@%s>" % (s.hexdigest(), openobject_id, 'syleam6.syleam.fr')


message = Object(cnx, 'mailgate.message')
message_ids = message.search([('model','=','project.issue'),('message_id','=', False)])

print '%d message to update' % len(message_ids)

for m in message.read(message_ids, ['name', 'res_id']):
    args = {'message_id': generate_tracking_message_id(m['res_id'])}
    message.write([m['id']], args)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
