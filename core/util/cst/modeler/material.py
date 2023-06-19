from core.util.cst.vb import modeler


def define_material(mws, name, epsilon, mu, tand, folder="", color=(0, 1, 1)):
    modeler.define_material(mws.modeler, name, epsilon, mu, tand, folder, color)


def load_material(mws, name):
    modeler.load_material(mws.modeler, name)
