from core.util.cst import modeler as c_modeler


# 优化后的网格建模函数速度已经大大提升
# 有些规则结构就算单独写建模函数，其速度提升也较为有限了
# 将来的结构不是特别必要，一般来说都会直接调用这个函数进行建模
def generate_grid(mws, material, matrix, step, z1, z2, component="Metal", name="default"):
    return c_modeler.shape.create_grid_by_matrix(mws, material, matrix, step, z1, z2, component, name)


def jerusalem_cross(mws, material, step, z1, z2, l, w, el, ew, component="Metal", name="default"):
    l = l + 1 if l % 2 != 0 else l
    w = w + 1 if w % 2 != 0 else w
    el = el + 1 if el % 2 != 0 else el

    x1 = int(-(w / 2)) * step
    x2 = int(w / 2) * step
    y1 = int(-(l / 2)) * step
    y2 = int(l / 2) * step
    c_modeler.shape.create_brick(mws, name, material, x1, x2, y1, y2, z1, z2, component)

    x1 = int(-(el / 2)) * step
    x2 = int(el / 2) * step
    y1 = int(l / 2) * step
    y2 = int(l / 2 + ew) * step
    c_modeler.shape.create_brick(mws, "edge", material, x1, x2, y1, y2, z1, z2, component)

    c_modeler.transform.mirror(mws, component, "edge", (0, 1, 0), copy=True, merge=True)
    c_modeler.bool.add(mws, component, name, component, "edge")
    c_modeler.transform.rotate(mws, component, name, (0, 0, 90), copy=True, merge=True)

    return component, name


# 单开口方环
# 由于之前三个模型的建模速度过于缓慢，发现是由于通过网格建模造成的
# 所以之后对于简单的模型，单独写建模函数，对于复杂的模型，调用网格生成的建模函数
# 但是无论对于哪种建模方式，都要 100% 保证建模和矩阵的对应，不能出现偏差
# step 存在的意义是希望输入的尺寸参数可以和生成矩阵的输入参数相同，依然是为了和矩阵做到对应,大部分时候 step 都是 1，不用刻意运算
def single_split_square_ring(mws, material, step, z1, z2, l, w, e, x, component="Metal", name="default"):
    if l % 2 != 0:
        l = l + 1

    x1 = int(-(l / 2)) * step
    x2 = int(l / 2) * step
    y1 = int(-(l / 2)) * step
    y2 = int(l / 2) * step
    c_modeler.shape.create_brick(mws, name, material, x1, x2, y1, y2, z1, z2, component)

    x1 = int(-((l - 2 * w) / 2)) * step
    x2 = int((l - 2 * w) / 2) * step
    y1 = int(-((l - 2 * w) / 2)) * step
    y2 = int((l - 2 * w) / 2) * step
    c_modeler.shape.create_brick(mws, "hole", material, x1, x2, y1, y2, z1, z2, component)

    x1 = int((l - 2 * w) / 2) * step
    x2 = int((l - 2 * w) / 2 + w) * step
    y1 = int(-((l - 2 * w) / 2) + e) * step
    y2 = int(-((l - 2 * w) / 2) + e + x) * step
    c_modeler.shape.create_brick(mws, "open_hole", material, x1, x2, y1, y2, z1, z2, component)

    c_modeler.bool.subtract(mws, component, name, component, "hole")
    c_modeler.bool.subtract(mws, component, name, component, "open_hole")

    return component, name
