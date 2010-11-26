# -*- coding: utf-8 -*-
##############################################################################
#
#    oobjlib module for OpenERP,
#    Copyright (C) 2010 SYLEAM Info Services (<http://www.syleam.fr/>)
#              Christophe CHAUVET <christophe.chauvet@syleam.fr>
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
import locale


def Format_Date(datum, date_style):
    """
    Convert date in input to an OpenObject format

    :param datum: string representation of the date in input
    :type  datum: str
    :param date_style: date format in input
    :type  date_style: str
    :return: date convert for OpenObject
    :rtype: str
    """
    try:
        return time.strftime('%Y-%m-%d', time.strptime(datum, date_style))
    except ValueError:
        return False


def Locale_Float(number, loc='en_US'):
    """
    Convert the locale number to a float

    :param number: Number representation in locale
    :type  number: str
    :param loc: Customer locale
    :type  loc: str
    """
    # Complete locale with encoding if necessary
    if loc.find('.') == -1:
        loc += '.utf-8'
    try:
        locale.setlocale(locale.LC_ALL, loc)
    except locale.Error:
        raise Exception('Unsuported locale (%s)' % loc)
    return  locale.atof(number)


def Locale_Date(datum, loc='en_US'):
    """
    Convert the locale number to a float

    :type  number: str
    :param number: Date representation in locale
    :type  loc: str
    :param loc: Customer locale
    """
    # Complete locale with encoding if necessary
    if loc.find('.') == -1:
        loc += '.utf-8'
    try:
        locale.setlocale(locale.LC_ALL, loc)
    except locale.Error:
        raise Exception('Unsuported locale (%s)' % loc)
    return Format_Date(datum, locale.nl_langinfo(locale.D_FMT))


def test():
    try:
        # Convert french date to openobject format
        assert Format_Date('03/02/2010', '%d/%m/%Y') == '2010-02-03'
        # Convert french float to a python float
        assert Locale_Float('5,5', 'fr_FR') == 5.5
        # Convert number with thousand separator to a python float
        assert Locale_Float('1,987.90') == 1987.90
        # Convert french date in openobject format
        assert Locale_Date('19/02/2009', 'fr_FR') == '2009-02-19'
        print 'Test Done'
    except AssertionError, e:
        print "Error: %r" % e

if __name__ == '__main__':
    test()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
