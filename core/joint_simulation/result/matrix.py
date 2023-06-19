import os
import numpy as np

from core.util.matrix import operation as m_operation
from core import global_var

output_dir = global_var.output_dir


def save_data(matrix, dir, name):
    save_dir = os.path.join(output_dir, dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_path = os.path.join(save_dir, name)
    np.savetxt(file_path, matrix, fmt="%d", delimiter=" ")


def save_data_by_layer(batch, mats, layer=1, dir_project="default_Project", prefix="", suffix=".txt"):
    for i in range(layer):
        mat = mats[i]
        i = i + 1
        save_data(mat, os.path.join(dir_project, str(batch) + "_batch", "matrix", "data", "layer_" + str(i)),
                  prefix + "_" + "mat_data" + suffix)


def save_pic(matrix, dir, name):
    m_operation.show.save_show_pic_rat90(matrix, isSave=True, dir=dir, name=name, isShow=False)


def save_pic_by_layer(batch, mats, layer=1, dir_project="default_Project", prefix="", suffix=""):
    for i in range(layer):
        mat = mats[i]
        i = i + 1
        save_pic(mat, os.path.join(dir_project, str(batch) + "_batch", "matrix", "pic", "layer_" + str(i)),
                 prefix + "_" + "mat_pic" + suffix)
