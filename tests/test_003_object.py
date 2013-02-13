# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenObject-Library, OpenERP Client Connection
#    Copyright (C) 2013 SYLEAM (<http://syleam.fr>) Christophe CHAUVET
#
#    This file is a part of OpenObject-Library
#
#    OpenObject-Library is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    OpenObject-Library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from common import OERPHOST, OERPPORT, OERPUSER, OERPPASS, OERPNAME
from oobjlib.connection import Connection
from oobjlib.component import Object
from oobjlib.exceptions import OObjlibException

import pytest


def setup_module(module):
    try:
        module.TestObject.cnx = Connection(
            server=OERPHOST,
            port=OERPPORT,
            dbname=OERPNAME,
            login=OERPUSER,
            password=OERPPASS)
    except OObjlibException, e:
        pytest.fail('Error %s' % e.message)


class TestObject(object):

    def test_res_partner(self):
        try:
            partner = Object(self.cnx, 'res.partner')
            mod_ids = partner.search([('customer', '=', True)])
            assert len(mod_ids) >= 1
            current_partner = partner.read(mod_ids[0], ['name'])
        except OObjlibException, e:
            pytest.fail(e.message)

    def test_res_partner_view(self):
        try:
            partner = Object(self.cnx, 'res.partner')
            partner.fields_view_get()
        except OObjlibException, e:
            pytest.fail(e.message)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
