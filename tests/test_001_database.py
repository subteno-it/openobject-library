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

from common import OERPHOST, OERPPORT, OERPNAME
from oobjlib.connection import Database
from oobjlib.exceptions import OObjlibException

import pytest


class TestDatabase(object):

    def test_database_list(self):
        try:
            db = Database(server=OERPHOST, port=OERPPORT)
            dblist = db.list()
        except OObjlibException, e:
            pytest.fail(e.message)

        assert isinstance(dblist, list)
        assert OERPNAME in dblist

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
