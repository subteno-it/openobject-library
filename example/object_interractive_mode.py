#!/usr/bin/python
# --*- coding: utf-8 -*-
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
This script enable a connection to the openerp server and
And stay in interractive mode (use python -i to do this)
"""

import sys
import code
sys.path.append('../')

from oobjlib.connection import Connection
from oobjlib.component import Object, Wizard, Workflow, Report
from oobjlib.common import GetParser
from optparse import OptionGroup

parser = GetParser('Interractive mode', '0.1')

group = OptionGroup(parser, "Object arguments",
        "Application Options")
group.add_option('-m', '--model', dest='model',
                 default='',
                 help='Enter the model name in OpenObject')
parser.add_option_group(group)

try:
    opts, args = parser.parse_args()
except SystemExit:
    sys.exit(0)

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

code.interact()

print 80 * '*'
print '* A connection was established to %s on database %s with user %s ' % (opts.server, opts.dbname, opts.user)
print '* Use "cnx" variable for the current connection'
print "* To create a new object: eg x = Object(cnx, 'res.partner')"
print "* To call a method on this object just execute x.search([('field','operator','value')])"
print '*'

if opts.model:
    obj = Object(cnx, opts.model)
    print '* "obj" variable is affect to "%s" object' % opts.model
    print "* To call a method on this object just execute obj.search([('field','operator','value')])"
    print '*'

print 80 * '*'
print '* To exit: enter "exit()" or press "Ctrl + D"'
print 80 * '*'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
