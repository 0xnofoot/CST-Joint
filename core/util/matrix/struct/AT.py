import numpy as np
from core.util.matrix.operation import bool as m_bool


# 与cst.struct中的 dorr_unilateral 对应，用于得到同一结构参数下的矩阵数据
# 实际上这种生成方式的限制条件过多，如果不加条件优化，不宜使用
# 返回：上下两个矩阵数据
def dorr_unilateral(n_size, l, w, p1, p2, offset):
    matrix_up = np.zeros((n_size, n_size))

    n_size_offset = int(n_size / 2)

    x1 = int(-(offset + w)) + n_size_offset
    x2 = int(-offset) + n_size_offset
    y1 = int(-(l / 2)) + n_size_offset
    y2 = int(l / 2) + n_size_offset
    matrix_up[x1:x2, y1:y2] = 1

    x1 = int(-offset) + n_size_offset
    x2 = int(-(offset - p1)) + n_size_offset
    y1 = int(l / 2 - w) + n_size_offset
    y2 = int(l / 2) + n_size_offset
    matrix_up[x1:x2, y1:y2] = 1

    x1 = int(-offset) + n_size_offset
    x2 = int(-(offset - p2)) + n_size_offset
    y1 = int(-(l / 2)) + n_size_offset
    y2 = int(-(l / 2 - w)) + n_size_offset
    matrix_up[x1:x2, y1:y2] = 1

    # matrix_up = matrix_up + np.rot90(matrix_up, 2)

    matrix_down = np.flip(matrix_up, axis=0)
    matrix_down = np.rot90(matrix_down, 1)

    return matrix_up, matrix_down


# 与cst.struct中的 dorr 对应，用于得到同一结构参数下的矩阵数据
# 相较于上面这个函数， 此函数是双开口环的传统生成方案，更可靠
# 返回：上下两个矩阵数据
def dorr(n_size, l, w, g, s):
    # 与cst.struct中的dorr生成函数作用相同
    if l % 2 != 0:
        l = l + 1

    base = np.zeros((n_size, n_size))
    empty = np.zeros((n_size, n_size))
    hole = np.zeros((n_size, n_size))

    n_size_offset = int(n_size / 2)

    x1 = int(-(l / 2)) + n_size_offset
    x2 = int(l / 2) + n_size_offset
    y1 = int(-(l / 2)) + n_size_offset
    y2 = int(l / 2) + n_size_offset
    base[x1:x2, y1:y2] = 1

    x1 = int(-((l - 2 * w) / 2)) + n_size_offset
    x2 = int((l - 2 * w) / 2) + n_size_offset
    y1 = int(-((l - 2 * w) / 2)) + n_size_offset
    y2 = int((l - 2 * w) / 2) + n_size_offset
    empty[x1:x2, y1:y2] = 1

    x1 = int(-(l / 2 - w - s)) + n_size_offset
    x2 = int((-(l / 2 - w - s)) + g) + n_size_offset
    y1 = int(-(l / 2)) + n_size_offset
    y2 = int((-(l / 2)) + w) + n_size_offset
    hole[x1:x2, y1:y2] = 1

    hole_rot = np.rot90(hole, 2)

    dorr_mat_up = m_bool.subtract(base, empty, hole_rot, hole)

    dorr_mat_down = np.flip(dorr_mat_up, axis=0)
    dorr_mat_down = np.rot90(dorr_mat_down, 1)

    return dorr_mat_up, dorr_mat_down
