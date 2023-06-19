import os
import re

from core.util.cst.vb import result


def get(file_path, sParam, allow_interactive=True):
    data = result.get_sParameters(file_path, sParam, allow_interactive)
    sParam_data = list(map(lambda t: t[:2], data))
    return sParam_data


def get_Zmax1_Zmax1(file_path):
    data = get(file_path, "SZmax(1),Zmax(1)")
    return data


def get_Zmax2_Zmax1(file_path):
    data = get(file_path, "SZmax(2),Zmax(1)")
    return data


def get_Zmin1_Zmax1(file_path):
    data = get(file_path, "SZmin(1),Zmax(1)")
    return data


def get_Zmin2_Zmax1(file_path):
    data = get(file_path, "SZmin(2),Zmax(1)")
    return data


def get_Zmax1_Zmax2(file_path):
    data = get(file_path, "SZmax(1),Zmax(2)")
    return data


def get_Zmax2_Zmax2(file_path):
    data = get(file_path, "SZmax(2),Zmax(2)")
    return data


def get_Zmin1_Zmax2(file_path):
    data = get(file_path, "SZmin(1),Zmax(2)")
    return data


def get_Zmin2_Zmax2(file_path):
    data = get(file_path, "SZmin(2),Zmax(2)")
    return data


def get_Zmax1_Zmin1(file_path):
    data = get(file_path, "SZmax(1),Zmin(1)")
    return data


def get_Zmax2_Zmin1(file_path):
    data = get(file_path, "SZmax(2),Zmin(1)")
    return data


def get_Zmin1_Zmin1(file_path):
    data = get(file_path, "SZmin(1),Zmin(1)")
    return data


def get_Zmin2_Zmin1(file_path):
    data = get(file_path, "SZmin(2),Zmin(1)")
    return data


def get_Zmax1_Zmin2(file_path):
    data = get(file_path, "SZmax(1),Zmin(2)")
    return data


def get_Zmax2_Zmin2(file_path):
    data = get(file_path, "SZmax(2),Zmin(2)")
    return data


def get_Zmin1_Zmin2(file_path):
    data = get(file_path, "SZmin(1),Zmin(2)")
    return data


def get_Zmin2_Zmin2(file_path):
    data = get(file_path, "SZmin(2),Zmin(2)")
    return data


def get_all_Zmaxin(cst_filepath):
    Zmax1_Zmax1 = get_Zmax1_Zmax1(cst_filepath)
    Zmax2_Zmax1 = get_Zmax2_Zmax1(cst_filepath)
    Zmin1_Zmax1 = get_Zmin1_Zmax1(cst_filepath)
    Zmin2_Zmax1 = get_Zmin2_Zmax1(cst_filepath)
    Zmax1_Zmax2 = get_Zmax1_Zmax2(cst_filepath)
    Zmax2_Zmax2 = get_Zmax2_Zmax2(cst_filepath)
    Zmin1_Zmax2 = get_Zmin1_Zmax2(cst_filepath)
    Zmin2_Zmax2 = get_Zmin2_Zmax2(cst_filepath)

    sParam_Zmaxin = {"Zmax1_Zmax1": Zmax1_Zmax1,
                     "Zmax2_Zmax1": Zmax2_Zmax1,
                     "Zmin1_Zmax1": Zmin1_Zmax1,
                     "Zmin2_Zmax1": Zmin2_Zmax1,
                     "Zmax1_Zmax2": Zmax1_Zmax2,
                     "Zmax2_Zmax2": Zmax2_Zmax2,
                     "Zmin1_Zmax2": Zmin1_Zmax2,
                     "Zmin2_Zmax2": Zmin2_Zmax2}

    return sParam_Zmaxin
