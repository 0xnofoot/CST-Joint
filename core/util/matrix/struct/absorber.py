import math
import os.path

from core.util.matrix import operation as m_operation
from core import global_var
import numpy as np
import matplotlib.pyplot as plt
import cv2

output_dir = global_var.output_dir


# 竖条
# l 和 w 都必须是偶数
def vertical_bar(n_size, l, w):
    if l % 2 != 0:
        l = l + 1

    if w % 2 != 0:
        w = w + 1

    base = np.zeros((n_size, n_size))

    n_size_offset = int(n_size / 2)

    x1 = int(-(w / 2)) + n_size_offset
    x2 = int(w / 2) + n_size_offset
    y1 = int(-(l / 2)) + n_size_offset
    y2 = int(l / 2) + n_size_offset
    base[x1:x2, y1:y2] = 1

    return base


# 十字
# l 和 w 都必须是偶数
def cross(n_size, l, w):
    v_bar_mat = vertical_bar(n_size, l, w)
    h_bar_mat = np.rot90(v_bar_mat, 1)
    cross_mat = m_operation.bool.add(v_bar_mat, h_bar_mat)

    return cross_mat


# 耶路撒冷十字
def jerusalem_cross(n_size, l, w, el, ew):
    cross_mat = cross(n_size, l, w)

    l = l + 1 if l % 2 != 0 else l
    el = el + 1 if el % 2 != 0 else el

    edge_1 = np.zeros((n_size, n_size))

    n_size_offset = int(n_size / 2)

    x1 = int(-(el / 2)) + n_size_offset
    x2 = int(el / 2) + n_size_offset
    y1 = int(l / 2) + n_size_offset
    y2 = int(l / 2 + ew) + n_size_offset
    edge_1[x1:x2, y1:y2] = 1

    edge_2 = np.rot90(edge_1, 1)
    edge_3 = np.rot90(edge_2, 1)
    edge_4 = np.rot90(edge_3, 1)
    edge_mat = m_operation.bool.add(edge_1, edge_2, edge_3, edge_4)
    jerusalem_mat = m_operation.bool.add(cross_mat, edge_mat)

    return jerusalem_mat


# 方环
# l 必须是偶数
def square_ring(n_size, l, w):
    if l % 2 != 0:
        l = l + 1

    base = np.zeros((n_size, n_size))
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
    hole[x1:x2, y1:y2] = 1

    matrix = m_operation.bool.subtract(base, hole)

    return matrix


# 单开口方环
# l 必须是偶数
# e 是开口相对于底上边的偏移
# x 是开口的大小
def single_split_square_ring(n_size, l, w, e, x):
    if l % 2 != 0:
        l = l + 1

    base = np.zeros((n_size, n_size))
    hole = np.zeros((n_size, n_size))
    open_hole = np.zeros((n_size, n_size))

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
    hole[x1:x2, y1:y2] = 1

    x1 = int((l - 2 * w) / 2) + n_size_offset
    x2 = int((l - 2 * w) / 2 + w) + n_size_offset
    y1 = int(-((l - 2 * w) / 2) + e) + n_size_offset
    y2 = int(-((l - 2 * w) / 2) + e + x) + n_size_offset
    open_hole[x1:x2, y1:y2] = 1

    matrix = m_operation.bool.subtract(base, hole, open_hole)

    return matrix


# 圆形块
def circle_block(n_size, r):
    # 设置画布像素为 800x800
    fig = plt.figure(figsize=(8, 8))
    # 归一化半径
    r = r / n_size
    # 绘制圆形并填充黑色
    circle = plt.Circle((0.5, 0.5), r, color="black")
    fig.gca().add_artist(circle)
    plt.axis("off")
    # 暂时保存当前的图片
    plt.savefig(os.path.join(output_dir, "buffer_img.png"), bbox_inches="tight", pad_inches=0)
    plt.close("all")

    # opencv 读取之前保存的图片
    img = cv2.imread(os.path.join(output_dir, "buffer_img.png"), 0)
    # 降维至 64x64
    img = cv2.resize(img, (64, 64))
    # 阈值处理
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)[1]
    # 根据 img 读取为矩阵数据并归一化
    matrix = np.array(img)
    matrix[matrix == 0] = 1
    matrix[matrix == 255] = 0

    matrix = matrix.astype(np.float)

    return matrix


# 单圆环
# r1 大半径    r2 小半径
def single_torus(n_size, r1, r2):
    # 设置画布像素为 800x800
    fig = plt.figure(figsize=(8, 8))
    # 归一化半径
    r1 = r1 / n_size
    r2 = r2 / n_size

    # 绘制大圆形并填充黑色
    circle1 = plt.Circle((0.5, 0.5), r1, color="black")

    # 绘制小圆形并填充白色
    circle2 = plt.Circle((0.5, 0.5), r2, color="white")

    fig.gca().add_artist(circle1)
    fig.gca().add_artist(circle2)
    plt.axis("off")
    # 暂时保存当前的图片
    plt.savefig(os.path.join(output_dir, "buffer_img.png"), bbox_inches="tight", pad_inches=0)
    plt.close("all")

    # opencv 读取之前保存的图片
    img = cv2.imread(os.path.join(output_dir, "buffer_img.png"), 0)
    # 降维至 64x64
    img = cv2.resize(img, (64, 64))
    # 阈值处理
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)[1]
    # 根据 img 读取为矩阵数据并归一化
    matrix = np.array(img)
    matrix[matrix == 0] = 1
    matrix[matrix == 255] = 0

    matrix = matrix.astype(np.float)

    return matrix


# 双圆环
# 外圆环：r1 大半径    r2 小半径
# 内圆环：r3 大半径    r4 小半径
def double_torus(n_size, r1, r2, r3, r4):
    torus_out_mat = single_torus(n_size, r1, r2)
    torus_in_mat = single_torus(n_size, r3, r4)

    matrix = m_operation.bool.add(torus_out_mat, torus_in_mat)

    return matrix


# 单开口圆环
# r1 大半径    r2 小半径
# proportion 开口占比
def open_single_ring(n_size, r1, r2, proportion):
    # 设置画布像素为 800x800
    fig = plt.figure(figsize=(8, 8))
    # 归一化半径
    r1 = r1 / n_size
    r2 = r2 / n_size

    # 绘制大圆形并填充黑色
    circle1 = plt.Circle((0.5, 0.5), r1, color="black")
    fig.gca().add_artist(circle1)

    # 绘制小圆形并填充白色
    circle2 = plt.Circle((0.5, 0.5), r2, color="white")
    fig.gca().add_artist(circle2)
    plt.axis("off")
    # 暂时保存当前的图片
    plt.savefig(os.path.join(output_dir, "buffer_img_1.png"), bbox_inches="tight", pad_inches=0)
    plt.close("all")

    # 重新设置画布像素为 800x800
    plt.figure(figsize=(8, 8))
    proportion = proportion + 1 if proportion % 2 != 0 else proportion
    datax = [proportion / 2, 100 - proportion, proportion / 2]
    # colorx = ["black", "white", "black"]
    colorx = ["black", "white", "black"]

    # 绘制扇形
    # 实际上绘制扇形的函数中 radius 参数具体如何设置暂时还是不太了解
    # 但是对于这个应用来说给一个极大值能到占满整个画布就够了，因此给了 10
    plt.pie(datax, colors=colorx, radius=2)

    plt.axis("off")
    # 暂时保存当前的图片
    plt.savefig(os.path.join(output_dir, "buffer_img_2.png"), bbox_inches="tight", pad_inches=0)
    plt.close("all")

    # opencv 读取之前保存的图片 1
    img1 = cv2.imread(os.path.join(output_dir, "buffer_img_1.png"), 0)
    img1 = cv2.resize(img1, (640, 640))
    # 阈值处理
    img1 = cv2.threshold(img1, 0, 255, cv2.THRESH_BINARY)[1]
    matrix_1 = np.array(img1)
    matrix_1[matrix_1 == 0] = 1
    matrix_1[matrix_1 == 255] = 0

    # opencv 读取之前保存的图片 2
    img2 = cv2.imread(os.path.join(output_dir, "buffer_img_2.png"), 0)
    img2 = cv2.resize(img2, (640, 640))
    img2 = cv2.threshold(img2, 127, 255, cv2.THRESH_BINARY)[1]
    matrix_2 = np.array(img2)
    matrix_2[matrix_2 == 0] = 1
    matrix_2[matrix_2 == 255] = 0

    matrix_1 = matrix_1.astype(np.float)
    matrix_2 = matrix_2.astype(np.float)

    matrix = m_operation.bool.subtract(matrix_1, matrix_2)

    matrix = cv2.resize(matrix, (64, 64))

    return matrix


# 十字混合
# 前三个参数同十字参数
# ag_step: 环绕生长的迭代次数
# fileter_step: 矩阵过滤的迭代次数
# ag_count: 环绕生长 每次的激活数 一般来说取 1
# 参照参数：
# n_size = 64, l = 32(30,34,36), w = 8, ag_step = 20, filter_step = 3
# n_size = 64, l = 40(38,42,44), w = 10, ag_step = 30, filter_step = 4
# n_size = 64, l = 48(46,50,52), w = 12, ag_step = 40, filter_step = 5
def cross_mixing(n_size, l, w, ag_step, filter_step, ag_count=1):
    cross_mat = cross(n_size, l, w)
    cross_split_mat = np.hsplit(cross_mat, 2)[1]
    cross_split_mat = np.vsplit(cross_split_mat, 2)[0]

    n2 = int(n_size / 2)
    l2 = int(l / 2)
    w2 = int(w / 2)

    c1 = (n2 - l2, w2)
    c2 = (n2 - w2 - int((l2 - w2) / 2), w2)
    c3 = (n2 - w2, w2)
    c4 = (n2 - w2 - int((l2 - w2) / 2), w2 + int((l2 - w2) / 2))
    c5 = (n2 - w2, w2 + int((l2 - w2) / 2))
    c6 = (n2 - l2, l2)
    c7 = (n2 - w2, l2)

    c8 = (n2 - l2, w2 + int((l2 - w2) / 2))
    c9 = (n2 - w2 - int((l2 - w2) / 2), l2)

    matrix_1 = m_operation.fun.around_growth(n2, ag_count, ag_step, ac_brick_initial=c1)
    matrix_2 = m_operation.fun.around_growth(n2, ag_count, int(ag_step * 0.75), ac_brick_initial=c2)
    matrix_3 = m_operation.fun.around_growth(n2, ag_count, int(ag_step * 0.5), ac_brick_initial=c3)
    matrix_4 = m_operation.fun.around_growth(n2, ag_count, int(ag_step * 1), ac_brick_initial=c4)
    matrix_5 = m_operation.fun.around_growth(n2, ag_count, int(ag_step * 0.75), ac_brick_initial=c5)
    matrix_6 = m_operation.fun.around_growth(n2, ag_count, int(ag_step * 1.5), ac_brick_initial=c6)
    matrix_7 = m_operation.fun.around_growth(n2, ag_count, ag_step, ac_brick_initial=c7)

    matrix_8 = m_operation.fun.around_growth(n2, ag_count, int(ag_step * 0.75), ac_brick_initial=c8)
    matrix_9 = m_operation.fun.around_growth(n2, ag_count, int(ag_step * 0.75), ac_brick_initial=c9)

    quarter_mat = m_operation.bool.add(matrix_1, matrix_2, matrix_3, matrix_4, matrix_5, matrix_6, matrix_7, matrix_8,
                                       matrix_9)
    quarter_mat = m_operation.bool.add(quarter_mat, cross_split_mat)

    quarter_mat = m_operation.fun.filter_by_around(n2, quarter_mat, step=filter_step)

    # 镜像对称
    matrix_m = np.fliplr(quarter_mat)

    # 拼接
    matrix = np.hstack((matrix_m, quarter_mat))

    # 中心对称
    matrix_m = np.flip(matrix)

    # 拼接
    matrix = np.vstack((matrix, matrix_m))

    return matrix


# 方环混合
# 前三个参数同方环参数
# ag_step: 环绕生长的迭代次数
# fileter_step: 矩阵过滤的迭代次数
# ag_count: 环绕生长 每次的激活数 一般来说取 1
# 参照参数：
# n_size = 64, l = 28, w = 4, ag_step = 20, filter_step = 3
# n_size = 64, l = 36, w = 6, ag_step = 30, filter_step = 4
# n_size = 64, l = 44, w = 8, ag_step = 40, filter_step = 5
def square_ring_mixing(n_size, l, w, ag_step, filter_step, ag_count=1):
    cross_mat = square_ring(n_size, l, w)
    cross_split_mat = np.hsplit(cross_mat, 2)[1]
    cross_split_mat = np.vsplit(cross_split_mat, 2)[0]

    n2 = int(n_size / 2)
    l2 = int(l / 2)
    w2 = w

    c1 = (n2 - l2 + w2, n2 - int((n2 - l2) / 2))
    c2 = (n2 - l2 - 1, l2)
    c3 = (n2 - l2 + w2 + int((l2 - w2) / 2), l2)
    c4 = (int((n2 - l2) / 2), l2 - w2 - 1)
    c5 = (n2 - l2 + w2 + int((l2 - w2) / 2), l2 - w2 - 1)
    c6 = (n2 - l2 - 1, int((l2 - w2) / 2))
    c7 = (n2 - l2 + w2, int((l2 - w2) / 2))
    c8 = (n2 - l2 + w2 + int((l2 - w2) / 2), int((l2 - w2) / 2))

    matrix_1 = m_operation.fun.around_growth(n2, ag_count, ag_step, ac_brick_initial=c1)
    matrix_2 = m_operation.fun.around_growth(n2, ag_count, ag_step, ac_brick_initial=c2)
    matrix_3 = m_operation.fun.around_growth(n2, ag_count, ag_step, ac_brick_initial=c3)
    matrix_4 = m_operation.fun.around_growth(n2, ag_count, ag_step, ac_brick_initial=c4)
    matrix_5 = m_operation.fun.around_growth(n2, ag_count, ag_step, ac_brick_initial=c5)
    matrix_6 = m_operation.fun.around_growth(n2, ag_count, ag_step, ac_brick_initial=c6)
    matrix_7 = m_operation.fun.around_growth(n2, ag_count, ag_step, ac_brick_initial=c7)
    matrix_8 = m_operation.fun.around_growth(n2, ag_count, int(ag_step * 1.5), ac_brick_initial=c8)

    quarter_mat = m_operation.bool.add(matrix_1, matrix_2, matrix_3, matrix_4, matrix_5, matrix_6, matrix_7, matrix_8)
    quarter_mat = m_operation.bool.add(quarter_mat, cross_split_mat)

    quarter_mat = m_operation.fun.filter_by_around(n2, quarter_mat, step=filter_step)

    # # 边缘 5 个块需要手动恢复
    # # 所以手动恢复成 1
    # quarter_mat[n2 - l2][l2 - 1] = 1
    # quarter_mat[n2 - l2][0] = 1
    # quarter_mat[n2 - l2 + w2 - 1][0] = 1
    # quarter_mat[n2 - 1][l2 - w2] = 1
    # quarter_mat[n2 - 1][l2 - 1] = 1

    # 镜像对称
    matrix_m = np.fliplr(quarter_mat)

    # 拼接
    matrix = np.hstack((matrix_m, quarter_mat))

    # 中心对称
    matrix_m = np.flip(matrix)

    # 拼接
    matrix = np.vstack((matrix, matrix_m))

    return matrix


# 单圆环混合
# 前三个参数同单圆环参数
# ag_step: 环绕生长的迭代次数
# fileter_step: 矩阵过滤的迭代次数
# ag_count: 环绕生长 每次的激活数 一般来说取 1
# 参照参数：
# n_size = 64, r1 = 20, r2 = 16, ag_step = 30, filter_step = 3
# n_size = 64, r1 = 22, r2 = 17, ag_step = 35, filter_step = 4
# n_size = 64, r1 = 24, r2 = 18, ag_step = 40, filter_step = 5
def single_torus_mixing(n_size, r1, r2, ag_step, filter_step, ag_count=1):
    cross_mat = single_torus(n_size, r1, r2)
    cross_split_mat = np.hsplit(cross_mat, 2)[1]
    cross_split_mat = np.vsplit(cross_split_mat, 2)[0]

    n2 = int(n_size / 2)

    c1 = (n2 - int(r1 * math.sqrt(3) / 2), int(r1 * math.sqrt(3) / 2))
    c2 = (n2 - int(r1 / math.sqrt(2)) - 2, int(r1 / math.sqrt(2)) + 1)
    c3 = (n2 - int(r1 / 2 * math.sqrt(3)) - 2, int(r1 / 2))
    c4 = (n2 - int(r1 / 2) - 1, int(r1 / 2 * math.sqrt(3)) + 1)
    c5 = (n2 - int(r2 / 2 * math.sqrt(3)), int(r2 / 2) - 1)
    c6 = (n2 - int(r2 / 2), int(r2 / 2 * math.sqrt(3)) - 1)
    c7 = (n2 - int(r2 / 2) - 1, int(r2 / 2))
    c8 = (n2 - int(r2 / math.sqrt(2) / 2) - 1, int(r2 / math.sqrt(2) / 2))

    matrix_1 = m_operation.fun.around_growth(n2, ag_count, ag_step, ac_brick_initial=c1)
    matrix_2 = m_operation.fun.around_growth(n2, ag_count, ag_step, ac_brick_initial=c2)
    matrix_3 = m_operation.fun.around_growth(n2, ag_count, ag_step, ac_brick_initial=c3)
    matrix_4 = m_operation.fun.around_growth(n2, ag_count, ag_step, ac_brick_initial=c4)
    matrix_5 = m_operation.fun.around_growth(n2, ag_count, ag_step, ac_brick_initial=c5)
    matrix_6 = m_operation.fun.around_growth(n2, ag_count, ag_step, ac_brick_initial=c6)
    matrix_7 = m_operation.fun.around_growth(n2, ag_count, ag_step, ac_brick_initial=c7)
    matrix_8 = m_operation.fun.around_growth(n2, ag_count, int(ag_step * 2), ac_brick_initial=c8)

    quarter_mat = m_operation.bool.add(matrix_1, matrix_2, matrix_3, matrix_4, matrix_5, matrix_6, matrix_7, matrix_8)
    quarter_mat = m_operation.bool.add(quarter_mat, cross_split_mat)

    quarter_mat = m_operation.fun.filter_by_around(n2, quarter_mat, step=filter_step)

    # # 边缘 4 个块需要手动恢复
    # # 所以手动恢复成 1
    # quarter_mat[n2 - r1][0] = 1
    # quarter_mat[n2 - r2 - 1][0] = 1
    # quarter_mat[n2 - 1][r1 - 1] = 1
    # quarter_mat[n2 - 1][r2] = 1

    # 镜像对称
    matrix_m = np.fliplr(quarter_mat)

    # 拼接
    matrix = np.hstack((matrix_m, quarter_mat))

    # 中心对称
    matrix_m = np.flip(matrix)

    # 拼接
    matrix = np.vstack((matrix, matrix_m))

    return matrix


# 空十字生长
# 不给原始的十字填充，但是通过十字的参数选择内部的点进行初始生长
# 实现生长出类似十字的效果
# 相对于 mixing 的函数来说，like 类型函数脱离了原本的形态
# 只是期望于控制初始生长点来实现生成想要看到的样子
# 前三个参数同十字参数
# ag_step: 环绕生长的迭代次数
# fileter_step: 矩阵过滤的迭代次数
# ag_count: 环绕生长 每次的激活数 一般来说取 1
# 参照参数：
# n_size = 64, l = 16, w = 4, ag_step = 3, filter_step = 0 # small
# n_size = 64, l = 20, w = 5, ag_step = 4, filter_step = 0 # small
# n_size = 64, l = 24, w = 6, ag_step = 5, filter_step = 0 # small
# n_size = 64, l = 28, w = 7, ag_step = 6, filter_step = 0 # small

# n_size = 64, l = 32, w = 8, ag_step = 7, filter_step = 1
# n_size = 64, l = 32, w = 8, ag_step = 8, filter_step = 1
# n_size = 64, l = 32, w = 8, ag_step = 9, filter_step = 1

# n_size = 64, l = 36, w = 9, ag_step = 9, filter_step = 1
# n_size = 64, l = 36, w = 9, ag_step = 10, filter_step = 1
# n_size = 64, l = 36, w = 9, ag_step = 11, filter_step = 1

# n_size = 64, l = 40, w = 10, ag_step = 11, filter_step = 2
# n_size = 64, l = 40, w = 10, ag_step = 12, filter_step = 2
# n_size = 64, l = 40, w = 10, ag_step = 13, filter_step = 2

# n_size = 64, l = 44, w = 11, ag_step = 13, filter_step = 2
# n_size = 64, l = 44, w = 11, ag_step = 14, filter_step = 2
# n_size = 64, l = 44, w = 11, ag_step = 15, filter_step = 2

# n_size = 64, l = 48, w = 12, ag_step = 13, filter_step = 3 # large
# n_size = 64, l = 48, w = 12, ag_step = 14, filter_step = 3 # large
# n_size = 64, l = 48, w = 12, ag_step = 15, filter_step = 3 # large
def cross_like(n_size, l, w, ag_step, filter_step, ag_count=1):
    base_mat = np.zeros((n_size, n_size))

    quarter_mat = np.hsplit(base_mat, 2)[1]
    quarter_mat = np.vsplit(quarter_mat, 2)[0]

    n2 = int(n_size / 2)
    l2 = int(l / 2)
    w2 = int(w / 2)

    c_step = int(l2 / 4)
    x_base_c = (n2 - l2 - 1, 0)
    y_base_c = (n2 - 1, 0)

    c_list = []
    c_weight_list = [1.0] * 30

    weight_in_i = [2, 3, 4, 7, 8, 9, 12, 13, 14, 15, 16, 17, 20, 21, 22, 25, 26, 27]
    weight_out_i = [0, 1, 5, 6, 10, 11, 18, 19, 23, 24, 28, 29]
    in_weight = 0.6
    out_weight = 1.25

    for w_i in weight_in_i:
        c_weight_list[w_i] = in_weight
    for w_i in weight_out_i:
        c_weight_list[w_i] = out_weight

    for i in range(3):
        for j in range(5):
            c = (x_base_c[0] + c_step * j, x_base_c[1] + int(w2 / 2 * i))
            c_list.append(c)

    for i in range(3):
        for j in range(5):
            c = (y_base_c[0] - int(w2 / 2 * i), y_base_c[1] + c_step * j)
            c_list.append(c)

    for i in range(30):
        ag_mat = m_operation.fun.around_growth(n2, ag_count, int(ag_step * c_weight_list[i]),
                                               ac_brick_initial=c_list[i])
        quarter_mat = m_operation.bool.add(quarter_mat, ag_mat)

    quarter_mat = m_operation.fun.filter_by_around(n2, quarter_mat, step=filter_step)

    # 由于生成的形状会出现离边界近的小空洞
    # 在这里做一个手动补齐
    # 相当于给矩阵加了一个小十字骨架
    quarter_mat[n2 - l2: n2, 0:2] = 1
    quarter_mat[n2 - 2:n2, 0: l2] = 1

    quarter_mat = m_operation.fun.filter_by_around(n2, quarter_mat, step=1)

    # 镜像对称
    matrix_m = np.fliplr(quarter_mat)

    # 拼接
    matrix = np.hstack((matrix_m, quarter_mat))

    # 中心对称
    matrix_m = np.flip(matrix)

    # 拼接
    matrix = np.vstack((matrix, matrix_m))

    return matrix
