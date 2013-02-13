# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenObject Library
#    Copyright (C) 2009-2012 Syleam (<http://syleam.fr>). Christophe Chauvet
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
SetupTools configuration file
"""

#from distribute_setup import use_setuptools
#use_setuptools()

from setuptools import Command, setup
from oobjlib import release

import os


class run_audit(Command):
    """Audits source code using PyFlakes for following issues:
        - Names which are used but not defined or used before they are defined.
        - Names which are redefined without having been used.
    """
    description = "Audit source code with PyFlakes"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import os, sys
        try:
            import pyflakes.scripts.pyflakes as flakes
        except ImportError:
            print "Audit requires PyFlakes installed in your system."
            sys.exit(-1)

        warns = 0
        # Define top-level directories
        dirs = ('oobjlib', 'examples', 'scripts')
        for dir in dirs:
            for root, _, files in os.walk(dir):
                for file in files:
                    if file != '__init__.py' and file.endswith('.py') :
                        warns += flakes.checkPath(os.path.join(root, file))
        if warns > 0:
            print "Audit finished with total %d warnings." % warns
        else:
            print "No problems found in sourcecode."

def find_packages(base):
    """Find all package for this application

    :param base: root path of source.
    :return: Returns a list of subpackages suitable for setup() packages keyword.
    """
    ret = [base]
    for path in os.listdir(base):
        if path.startswith('.'):
            continue
        full_path = os.path.join(base, path)
        if os.path.isdir(full_path):
            ret += find_packages(full_path)
    return ret

if os.path.exists("README.rst"):
    import codecs
    LONG_DESCRIPTION = codecs.open('README.rst', "r", "utf-8").read()
else:
    LONG_DESCRIPTION = release.long_description

setup(
    name=release.appname,
    version='2.0.2-dev',
    description=release.description,
    long_description=LONG_DESCRIPTION,
    author=release.author,
    author_email=release.author_email,
    license='GPLv3',
    url=release.url,
    packages=find_packages('oobjlib'),
    classifiers=[i for i in release.classifiers.split("\n") if i],
    cmdclass={'audit': run_audit},
)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
