from os import path

def make_path_unixy(p):
    return p.replace('\\', "/")

config_helper_path = path.realpath(__file__)
#C:\django\qcumber\qcumber\qcumber_congfiguration.py

qcumber_root = path.dirname(path.dirname(config_helper_path))
#C:\django\qcumber

UNIX_QCUMBER_ROOT = make_path_unixy(qcumber_root)
#C:/django/qcumber

print('Qcumber located at %s' % UNIX_QCUMBER_ROOT)


QCUMBER_ADMIN_TEMPLATE_DIR = make_path_unixy(path.join(UNIX_QCUMBER_ROOT, "templates"))
#C:/django/qcumber/templates