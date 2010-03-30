# -*- coding: utf-8 -*-
##############################################################################
#
#    oobjlib module for OpenERP, 
#    Copyright (C) 2010 SYLEAM Info Services (<http://www.syleam.fr/>) 
#              Christophe CHAUVET
#
#    This file is a part of oobjlib
#
#    oobjlib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    oobjlib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""
Global convertion function
"""

import time

def Format_Date(datum, date_style):
    """
    Convert date in input to an OpenObject format

    @type  datum: str
    @param datum: string representation of the date in input
    @type  date_style: str
    @param date_style: date format in input
    @rtype: str
    @return: date convert for OpenObject
    """
    return time.strftime('%Y-%m-%d', time.strptime(datum, date_style))


def test():
    try:
        assert Format_Date('03/02/2010','%d/%m/%Y') == '2010-02-03'
        print 'Test Done'
    except AssetionError, e:
        print "Error: %r" % e

if __name__ == '__main__':
    test()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
