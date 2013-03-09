#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from distutils.core import setup

__author__ = "Benoît HERVIER"
__copyright__ = "Copyright 2013 " + __author__
__license__ = "GPLv3"
__version__ = "0.1.0"
__maintainer__ = "Benoît HERVIER"
__email__ = "khertan@khertan.net"
__status__ = "Beta"


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="gedit-autopep8-plugin",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description='GEdit-AutoPEP8 is a plugin to use AutoPEP8 inside GEdit',
    license="GPL",
    keywords="flake8 lint gedit",
    url="http://khertan.net/gedit_autopep8",
    install_require='autopep8 gedit',
    data_files=('/usr/lib/gedit/plugins', ['gedit_autopep8.plugin',
                                           'gedit_autopep8']),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 5 - Production/" + __status__,
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers", ],)

