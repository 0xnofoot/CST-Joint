from core.util.cst.vb import modeler


def translate(mws, component, name, vector, copy=False, merge=False):
    modeler.translate(mws.modeler, component, name, vector, copy, merge)


def rotate(mws, component, name, angle, center=(0, 0, 0), copy=False, merge=False):
    modeler.rotate(mws.modeler, component, name, center, angle, copy, merge)


def mirror(mws, component, name, plane, center=(0, 0, 0), copy=False, merge=False):
    modeler.mirror(mws.modeler, component, name, center, plane, copy, merge)


def rename(mws, component, name, new_name):
    modeler.rename(mws.modeler, component, name, new_name)
