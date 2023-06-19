from core.util.cst import modeler


# 创建一个矩形块基板, 该基板以（0,0）坐标为中心
# X: 基板的长度（x方向）
# Y: 基板的宽度（y方向）
# z1: 基板的厚度坐标（z方向）
# z2: 基板的厚度坐标（z方向）
# 由于画图时最好与矩阵对应，所以 X和 Y 的尺寸最好是偶数
# step: 每一个单位尺寸的步长，用来计算长度，z不参与计算
# 返回：该基板的器件和名字
def brick_sub(mws, material, X, Y, z1, z2, step, name="brick_sub", component="Substrate"):
    x1 = int(-(X / 2)) * step
    x2 = int(X / 2) * step
    y1 = int(-(Y / 2)) * step
    y2 = int(Y / 2) * step
    modeler.shape.create_brick(mws, name, material, x1, x2, y1, y2, z1, z2, component)

    return component, name
