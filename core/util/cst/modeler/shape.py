from core.util.cst.vb import modeler
import numpy as np


def create_brick(mws, name, material, x1_range, x2_range, y1_range, y2_range,
                 z1_range, z2_range, component="component1"):
    modeler.create_brick(mws.modeler, name, material, x1_range, x2_range, y1_range, y2_range,
                         z1_range, z2_range, component)


def delete_solid(mws, component, name):
    modeler.delete_solid(mws.modeler, component, name)


# # 通过矩阵生成CST模型，以（0，0）为中心
# def create_grid_by_matrix(mws, material, matrix, step, z1, z2, component, name):
#     x_size, y_size = np.shape(matrix)
#     x_start = -x_size / 2 * step
#     y_start = -y_size / 2 * step
#
#     count = 0
#     for index, value in np.ndenumerate(matrix):
#         if value == 0:
#             continue
#         count = count + 1
#         x, y = index
#         x1 = x_start + x * step
#         x2 = x1 + step
#         y1 = y_start + y * step
#         y2 = y1 + step
#
#         if count == 1:
#             create_brick(mws, name, material, x1, x2, y1, y2, z1, z2, component)
#         else:
#             i_name = name + "_grid_" + str(x) + "_" + str(y)
#             create_brick(mws, i_name, material, x1, x2, y1, y2, z1, z2, component)
#             modeler.bool_add(mws.modeler, component, name, component, i_name)
#
#     return component, name

# 优化后的 通过矩阵生成 CST 结构的函数
# 通过对每一列单独处理，实现每一列中相连的块只进行一次建模
# 肉眼可见的增加了建模速度
def create_grid_by_matrix(mws, material, matrix, step, z1, z2, component, name):
    x_size, y_size = np.shape(matrix)
    x_start = -x_size / 2 * step
    y_start = -y_size / 2 * step

    def get_brick_coor_list(coor):
        bl = []
        record_start = False

        # 坐标信息记录的缓存变量
        # brick_start: 目标块的开始坐标
        brick_start = 0
        # brick_len: 目标块的长度
        brick_len = 1

        for index, value in np.ndenumerate(coor):
            if value == 1 and record_start is False:
                record_start = True
                brick_start = index[0]
                if index[0] == y_size - 1:
                    bl.append((brick_start, brick_len))
            elif (value == 0 or index[0] == y_size - 1) and record_start is True:
                record_start = False
                if index[0] == y_size - 1 and value == 1:
                    brick_len = y_size - brick_start
                else:
                    brick_len = index[0] - brick_start
                bl.append((brick_start, brick_len))

        return bl

    model_start = True
    x_index = 0
    for x_coor in matrix:
        x1 = x_start + x_index * step
        x2 = x1 + step
        bricks_list = get_brick_coor_list(x_coor)
        for brick in bricks_list:
            y1 = y_start + brick[0] * step
            y2 = y1 + brick[1] * step

            if model_start is True:
                create_brick(mws, name, material, x1, x2, y1, y2, z1, z2, component)
                model_start = False
            else:
                i_name = name + "_grid_" + str(x1) + "_" + str(y1)
                create_brick(mws, i_name, material, x1, x2, y1, y2, z1, z2, component)
                modeler.bool_add(mws.modeler, component, name, component, i_name)
        x_index = x_index + 1
    return component, name
