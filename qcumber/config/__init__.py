# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from os import path

MISSING_MODULE_MESSAGE = '\nYou need to copy "qcumber/config/example_private_config.py" '\
    'to "qcumber/config/private_config.py" and customize it for your environment. '\
    'See the setup guide in the readme.'

def make_path_unixy(p):
    return p.replace('\\', "/")

def unixy_join(p1, p2):
    return make_path_unixy(path.join(p1, p2))

def unixy_project_path(p):
    return unixy_join(UNIX_QCUMBER_ROOT, p)

config_helper_path = path.realpath(__file__)
#C:\django\qcumber\qcumber\qcumber_congfiguration.py

qcumber_root = path.dirname(path.dirname(path.dirname(config_helper_path)))
#C:\django\qcumber

UNIX_QCUMBER_ROOT = make_path_unixy(qcumber_root)
#C:/django/qcumber
