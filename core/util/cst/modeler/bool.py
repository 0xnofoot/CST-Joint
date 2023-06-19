from core.util.cst.vb import modeler


def add(mws, component1, solid1, component2, solid2):
    modeler.bool_add(mws.modeler, component1, solid1, component2, solid2)


def subtract(mws, component1, solid1, component2, solid2):
    modeler.bool_subtract(mws.modeler, component1, solid1, component2, solid2)
