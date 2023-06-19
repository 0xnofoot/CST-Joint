from core.util.cst.vb import modeler


def save_params(mws, name, value):
    modeler.save_params(mws.modeler, name, value)
