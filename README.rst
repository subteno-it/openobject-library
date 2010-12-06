##############################
 oobjlib - OpenObject Library
##############################

:Version: 1.0.0

`openobject-library` is a library to interract with the OpenERP Framework, known as `OpenObject`_


.. _`OpenObject`: https://launchpad.net/openobject


Installation
============

You can install `oobjlib` either via the Python Package Index (PyPI)
or from source.

To install using `pip`,::

    $ pip install openobject-library

To install using `easy_install`,::

    $ easy_install openobject-library

If you have downloaded a source tarball you can install it
by doing the following,::

    $ python setup.py build
    $ sudo python setup.py install

If you want to develop a new functionnality, you can install it 
by doing the following (in python 2.6 or greater),::

    $ python setup.py develop --user

or simply::

    $ sudo python setup.py develop


Quick overview
==============

::

    import sys
    from oobjlib.connection import Database
    
    try:
        db = Database(server='localhost', port=8069)
    except Exception, e:
        print '%s' % repr(e)
        sys.exit(1)

    for d in db.list():
        print '* %s' % d

This example retrieve all databases and print one line per database


Licence
=======

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

