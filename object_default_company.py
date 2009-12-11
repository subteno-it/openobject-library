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
Verify the customization for an objet in this company
Only with OpenERP 5.2 and Greater
"""

from oobjlib.connection import Connection
from oobjlib.component import Object
from optparse import OptionParser, OptionGroup


usage = "Usage %prog [options]"
__version__ = '1.0'

parser = OptionParser(usage, prog='object_default_company.py',
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
group.add_option('-c', '--company', dest='company',
                default='',
                help='Enter list of companies, seprate by a comma (,)')
parser.add_option_group(group)

opts, args = parser.parse_args()

try:
    cnx = Connection(server=opts.server, dbname=opts.dbname, login=opts.user,
                     password=opts.passwd)
except Exception, e:
    print '%s' % str(e)
    exit(1)


user = Object(cnx, 'res.users')
multi = Object(cnx, 'res.company')

user_id = user.search([('login','=',opts.user)])[0]
# save company_id to restore it after 
curr = user.read(user_id, ['company_ids','company_id'])
c_save_id = curr['company_id']
print 'User: %d => %s (id %d)' % (user_id, c_save_id[1], c_save_id[0])

##
# If the company argument is missing, retrieve all companies in the user form
#
if opts.company:
    companies = opts.company.split(',')
else:
    companies = curr['company_ids']

s = 23
header = ('Main Company'.ljust(s), 'Object'.ljust(s), 'Dest Company'.ljust(s))

print 80 * '-'
print '| %s | %s | %s |' % header
print 80 * '-'
for i in companies:
    ##
    # Change company to the user, to test the rules
    #
    i = int(i)
    source = multi.read(i, ['name'])['name']
    try:
        user.write([user_id], {'company_id': i})
    except Exception, e:
        print '| %s | %s | %s |' % (source.ljust(s), s * '*', s * '*')
        continue

    ##
    # Read the company by default for this object
    #
    dest_id = multi._company_default_get(opts.model)
    dest = multi.read(dest_id, ['name'])['name']

    print '| %s | %s | %s |' % (source.ljust(s), opts.model.ljust(s), dest.ljust(s))

print 80 * '-'

user.write([user_id], {'company_id': c_save_id[0]})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
