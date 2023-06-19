from core.util.cst import modeler
from core import global_var

output_dir = global_var.output_dir


# |-----------------------------------------------------------|
# |                             |                             |
# | --|-----|-------------|     |                             |
# | ^ |     |<----p1----->|     |                             |
# | | |     |-------------|     |                             |
# | | |     |                   |                             |
# | | |     |                   |                             |
# | l |<-w->|                   |                             |
# | | |     |                   |                             |
# | | |     |<------offset----->|                             |
# | | |     |                   |                             |
# | | |     |--------|          |                             |
# | ^ |     |<--p2-->|          |                             |
# | --|-----|--------|          |                             |
# |                             |                             |
# |-----------------------------------------------------------|
#
# dorr: 双开口环
# 本函数用于在cst中创建一个双开口环结构, （双层）
# 与另外一种传统方法不同的是， 此函数先在一边创建一个形状，然后依靠旋转得到全部的结构
# 由于画图时最好与矩阵对应，所以 l 的尺寸最好是偶数
# th: 上下两结构之间的距离， t：结构的厚度
# 创建出的结构默认下结构的上表面为 z=0 的平面
# step: 每一个单位尺寸的步长，用来计算长度，th 和 t 不参与计算
# 返回：dorr 结构的器件和名字
# 实际上这种生成方式的限制条件过多，如果不加条件优化，不宜使用
def dorr_unilateral(mws, material, l, w, p1, p2, offset, th, t, step, name="dorr", component="Metal"):
    x1 = int(-(offset + w)) * step
    x2 = int(-offset) * step
    y1 = int(-(l / 2)) * step
    y2 = int(l / 2) * step
    z1 = -t
    z2 = 0
    modeler.shape.create_brick(mws, "solid_1", material, x1, x2, y1, y2, z1, z2, component)

    x1 = int(-offset) * step
    x2 = int(-(offset - p1)) * step
    y1 = int(l / 2 - w) * step
    y2 = int(l / 2) * step
    modeler.shape.create_brick(mws, "solid_2", material, x1, x2, y1, y2, z1, z2, component)

    x1 = int(-offset) * step
    x2 = int(-(offset - p2)) * step
    y1 = int(-(l / 2)) * step
    y2 = int(-(l / 2 - w)) * step
    modeler.shape.create_brick(mws, "solid_3", material, x1, x2, y1, y2, z1, z2, component)

    modeler.bool.add(mws, component, "solid_1", component, "solid_2")
    modeler.bool.add(mws, component, "solid_1", component, "solid_3")

    modeler.transform.rotate(mws, component, "solid_1", (0, 0, 180), copy=True, merge=True)
    modeler.transform.rename(mws, component, "solid_1", name)
    modeler.transform.translate(mws, component, name, (0, 0, th + t), copy=True, merge=True)

    # 没写完 上面一句有问题

    return component, name


# dorr(双开口环)的传统生成方式
def dorr(mws, material, l, w, g, s, th, t, step, name="dorr", component="Metal"):
    # 为了保证结构和矩阵可以无差别对应，在这里要做一次偶数处理
    # 实际上后续的计算操作看上去如此繁复，并不都是必要的
    # 只是为了完全保证二者的对应而已
    # 虽然这会降低 l 的随机性，但是是必要的
    if l % 2 != 0:
        l = l + 1

    x1 = int(-(l / 2)) * step
    x2 = int(l / 2) * step
    y1 = int(-(l / 2)) * step
    y2 = int(l / 2) * step
    z1 = -t
    z2 = 0
    modeler.shape.create_brick(mws, "base", material, x1, x2, y1, y2, z1, z2, component)

    x1 = int(-((l - 2 * w) / 2)) * step
    x2 = int((l - 2 * w) / 2) * step
    y1 = int(-((l - 2 * w) / 2)) * step
    y2 = int((l - 2 * w) / 2) * step
    modeler.shape.create_brick(mws, "empty", material, x1, x2, y1, y2, z1, z2, component)

    x1 = int(-(l / 2 - w - s)) * step
    x2 = int((-(l / 2 - w - s)) + g) * step
    y1 = int(-(l / 2)) * step
    y2 = int((-(l / 2)) + w) * step
    modeler.shape.create_brick(mws, "hole", material, x1, x2, y1, y2, z1, z2, component)

    modeler.transform.rotate(mws, component, "hole", (0, 0, 180), copy=True, merge=True)

    modeler.bool.subtract(mws, component, "base", component, "empty")
    modeler.bool.subtract(mws, component, "base", component, "hole")

    modeler.transform.translate(mws, component, "base", (0, 0, th + t), copy=True)
    modeler.transform.mirror(mws, component, "base", (0, 1, 0))
    modeler.transform.rotate(mws, component, "base", (0, 0, 90))

    modeler.bool.add(mws, component, "base", component, "base_1")
    modeler.transform.rename(mws, component, "base", name)

    return component, name