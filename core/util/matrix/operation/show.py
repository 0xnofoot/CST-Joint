import matplotlib.pyplot as plt
import numpy as np
import os
from core import global_var

output_dir = global_var.output_dir


# 以逆时针旋转 90°显示该矩阵
# isSave: 选择是否保存该图像
# isShow: 选择是否显示该图像
def save_show_pic_rat90(matrix, isSave=False, dir="default", name=None, isShow=True):
    matrix = np.rot90(matrix, 1)
    plt.matshow(matrix, cmap=plt.cm.Greys)
    plt.xticks(alpha=0)
    plt.yticks(alpha=0)
    plt.tick_params(axis='x', width=0)
    plt.tick_params(axis='y', width=0)
    # plt.grid()
    if isSave is True and name is not None:
        save_dir = os.path.join(output_dir, dir)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        file_path = os.path.join(save_dir, name)
        plt.savefig(file_path)
    if isShow is True:
        plt.show()

    plt.close("all")


def save_data(name, matrix, dir=None):
    save_dir = os.path.join(output_dir, "matrix", "data", dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, name + ".txt")

    # 矩阵以 %d 数据类型保存，并以" "做分隔符保存到 test.txt文件中
    np.savetxt(save_path, matrix, fmt="%d", delimiter=" ")
