from core.util.matrix import struct as m_struct, operation as m_operation
from core.util.cst import modeler as c_modeler, struct as c_struct, result as c_result


# ！！！: 返回的 info 标准：
# info 是一个信息字典， 用于返回这一次仿真中所有的数据信息
# 其中包括
# info["struct_param"] : 结构参数信息， 结构参数本身也是一个字典
# info["matrix_data"]     : 矩阵数据信息，是一个元组，因为可能有多层矩阵
# info["struct_name"]  : 结构器件和名称信息，是一个元组
# info["sParam"]       : S 参数数据信息，是一个字典

# 竖条
def vertical_bar(mws, cst_file_path, n_size, l, w, t, th, step=1):
    info = {}

    struct_param = {"n_size": n_size, "l": l, "w": w, "t": t, "th": th}
    info["struct_param"] = struct_param

    matrix = m_struct.absorber.vertical_bar(n_size, l, w)

    info["matrix_data"] = (matrix,)

    c_modeler.material.load_material(mws, "Gold")
    c_modeler.material.load_material(mws, "PTFE (lossy)")

    c_modeler.solver.boundary(mws, Zmin="electric")

    metal_sub_name = c_struct.substrate.brick_sub(mws, "Gold", n_size, n_size, 0, t, step, name="metal_sub")
    medium_sub_name = c_struct.substrate.brick_sub(mws, "PTFE (lossy)", n_size, n_size, t, t + th, step,
                                                   name="medium_sub")
    absorb_name = c_struct.absorber.generate_grid(mws, "Gold", matrix, step, t + th, t + th + t, name="vertical_bar")
    info["struct_name"] = (metal_sub_name, medium_sub_name, absorb_name)

    isComplete = c_modeler.solver.run(mws)

    if isComplete is not True:
        print("run failed")
        return

    # 返回 S 参数，对于单极化的吸收器来说，只需要一种 S参数的数据，SZmax(1),Zmax(1)
    sParam_Zmax1_Zmax1 = c_result.sParam.get_Zmax1_Zmax1(cst_file_path)
    sParam = {"Zmax1_Zmax1": sParam_Zmax1_Zmax1}
    info["sParam"] = sParam

    c_modeler.shape.delete_solid(mws, metal_sub_name[0], metal_sub_name[1])
    c_modeler.shape.delete_solid(mws, medium_sub_name[0], medium_sub_name[1])
    c_modeler.shape.delete_solid(mws, absorb_name[0], absorb_name[1])

    return info


# 十字
def cross(mws, cst_file_path, n_size, l, w, t, th, step=1):
    info = {}

    struct_param = {"n_size": n_size, "l": l, "w": w, "t": t, "th": th}
    info["struct_param"] = struct_param

    matrix = m_struct.absorber.cross(n_size, l, w)

    info["matrix_data"] = (matrix,)

    c_modeler.material.load_material(mws, "Gold")
    c_modeler.material.load_material(mws, "PTFE (lossy)")

    c_modeler.solver.boundary(mws, Zmin="electric")

    metal_sub_name = c_struct.substrate.brick_sub(mws, "Gold", n_size, n_size, 0, t, step, name="metal_sub")
    medium_sub_name = c_struct.substrate.brick_sub(mws, "PTFE (lossy)", n_size, n_size, t, t + th, step,
                                                   name="medium_sub")
    absorb_name = c_struct.absorber.generate_grid(mws, "Gold", matrix, step, t + th, t + th + t, name="cross")
    info["struct_name"] = (metal_sub_name, medium_sub_name, absorb_name)

    isComplete = c_modeler.solver.run(mws)

    if isComplete is not True:
        print("run failed")
        return

    # 返回 S 参数，对于单极化的吸收器来说，只需要一种 S参数的数据，SZmax(1),Zmax(1)
    sParam_Zmax1_Zmax1 = c_result.sParam.get_Zmax1_Zmax1(cst_file_path)
    sParam = {"Zmax1_Zmax1": sParam_Zmax1_Zmax1}
    info["sParam"] = sParam

    c_modeler.shape.delete_solid(mws, metal_sub_name[0], metal_sub_name[1])
    c_modeler.shape.delete_solid(mws, medium_sub_name[0], medium_sub_name[1])
    c_modeler.shape.delete_solid(mws, absorb_name[0], absorb_name[1])

    return info


# 耶路撒冷十字
def jerusalem_cross(mws, cst_file_path, n_size, l, w, el, ew, t, th, step=1):
    info = {}

    struct_param = {"n_size": n_size, "l": l, "w": w, "el": el, "ew": ew, "t": t, "th": th}
    info["struct_param"] = struct_param

    matrix = m_struct.absorber.jerusalem_cross(n_size, l, w, el, ew)

    info["matrix_data"] = (matrix,)

    c_modeler.material.load_material(mws, "Gold")
    c_modeler.material.load_material(mws, "PTFE (lossy)")

    c_modeler.solver.boundary(mws, Zmin="electric")

    metal_sub_name = c_struct.substrate.brick_sub(mws, "Gold", n_size, n_size, 0, t, step, name="metal_sub")
    medium_sub_name = c_struct.substrate.brick_sub(mws, "PTFE (lossy)", n_size, n_size, t, t + th, step,
                                                   name="medium_sub")
    absorb_name = c_struct.absorber.jerusalem_cross(mws, "Gold", step, t + th, t + th + t, l, w, el, ew,
                                                    name="jerusalem_cross")
    info["struct_name"] = (metal_sub_name, medium_sub_name, absorb_name)

    isComplete = c_modeler.solver.run(mws)

    if isComplete is not True:
        print("run failed")
        return

    # 返回 S 参数，对于单极化的吸收器来说，只需要一种 S参数的数据，SZmax(1),Zmax(1)
    sParam_Zmax1_Zmax1 = c_result.sParam.get_Zmax1_Zmax1(cst_file_path)
    sParam = {"Zmax1_Zmax1": sParam_Zmax1_Zmax1}
    info["sParam"] = sParam

    c_modeler.shape.delete_solid(mws, metal_sub_name[0], metal_sub_name[1])
    c_modeler.shape.delete_solid(mws, medium_sub_name[0], medium_sub_name[1])
    c_modeler.shape.delete_solid(mws, absorb_name[0], absorb_name[1])

    return info


# 方环
def square_ring(mws, cst_file_path, n_size, l, w, t, th, step=1):
    info = {}

    struct_param = {"n_size": n_size, "l": l, "w": w, "t": t, "th": th}
    info["struct_param"] = struct_param

    matrix = m_struct.absorber.square_ring(n_size, l, w)

    info["matrix_data"] = (matrix,)

    c_modeler.material.load_material(mws, "Gold")
    c_modeler.material.load_material(mws, "PTFE (lossy)")

    c_modeler.solver.boundary(mws, Zmin="electric")

    metal_sub_name = c_struct.substrate.brick_sub(mws, "Gold", n_size, n_size, 0, t, step, name="metal_sub")
    medium_sub_name = c_struct.substrate.brick_sub(mws, "PTFE (lossy)", n_size, n_size, t, t + th, step,
                                                   name="medium_sub")
    absorb_name = c_struct.absorber.generate_grid(mws, "Gold", matrix, step, t + th, t + th + t, name="square_ring")
    info["struct_name"] = (metal_sub_name, medium_sub_name, absorb_name)

    isComplete = c_modeler.solver.run(mws)

    if isComplete is not True:
        print("run failed")
        return

    # 返回 S 参数，对于单极化的吸收器来说，只需要一种 S参数的数据，SZmax(1),Zmax(1)
    sParam_Zmax1_Zmax1 = c_result.sParam.get_Zmax1_Zmax1(cst_file_path)
    sParam = {"Zmax1_Zmax1": sParam_Zmax1_Zmax1}
    info["sParam"] = sParam

    c_modeler.shape.delete_solid(mws, metal_sub_name[0], metal_sub_name[1])
    c_modeler.shape.delete_solid(mws, medium_sub_name[0], medium_sub_name[1])
    c_modeler.shape.delete_solid(mws, absorb_name[0], absorb_name[1])

    return info


# 单开口方环
def single_split_square_ring(mws, cst_file_path, n_size, l, w, e, x, t, th, step=1):
    info = {}

    struct_param = {"n_size": n_size, "l": l, "w": w, "e": e, "x": x, "t": t, "th": th}
    info["struct_param"] = struct_param

    matrix = m_struct.absorber.single_split_square_ring(n_size, l, w, e, x)

    info["matrix_data"] = (matrix,)

    c_modeler.material.load_material(mws, "Gold")
    c_modeler.material.load_material(mws, "PTFE (lossy)")

    c_modeler.solver.boundary(mws, Zmin="electric")

    metal_sub_name = c_struct.substrate.brick_sub(mws, "Gold", n_size, n_size, 0, t, step, name="metal_sub")
    medium_sub_name = c_struct.substrate.brick_sub(mws, "PTFE (lossy)", n_size, n_size, t, t + th, step,
                                                   name="medium_sub")

    absorb_name = c_struct.absorber.single_split_square_ring(mws, "Gold", step, t + th, t + th + t, l, w, e, x,
                                                             name="single_split_square_ring")
    info["struct_name"] = (metal_sub_name, medium_sub_name, absorb_name)

    isComplete = c_modeler.solver.run(mws)

    if isComplete is not True:
        print("run failed")
        return

    # 返回 S 参数，对于单极化的吸收器来说，只需要一种 S参数的数据，SZmax(1),Zmax(1)
    sParam_Zmax1_Zmax1 = c_result.sParam.get_Zmax1_Zmax1(cst_file_path)
    sParam = {"Zmax1_Zmax1": sParam_Zmax1_Zmax1}
    info["sParam"] = sParam

    c_modeler.shape.delete_solid(mws, metal_sub_name[0], metal_sub_name[1])
    c_modeler.shape.delete_solid(mws, medium_sub_name[0], medium_sub_name[1])
    c_modeler.shape.delete_solid(mws, absorb_name[0], absorb_name[1])

    return info


# 圆形块
def circle_block(mws, cst_file_path, n_size, r, t, th, step=1):
    info = {}

    struct_param = {"n_size": n_size, "r": r, "t": t, "th": th}
    info["struct_param"] = struct_param

    matrix = m_struct.absorber.circle_block(n_size, r)

    info["matrix_data"] = (matrix,)

    c_modeler.material.load_material(mws, "Gold")
    c_modeler.material.load_material(mws, "PTFE (lossy)")

    c_modeler.solver.boundary(mws, Zmin="electric")

    metal_sub_name = c_struct.substrate.brick_sub(mws, "Gold", n_size, n_size, 0, t, step, name="metal_sub")
    medium_sub_name = c_struct.substrate.brick_sub(mws, "PTFE (lossy)", n_size, n_size, t, t + th, step,
                                                   name="medium_sub")
    absorb_name = c_struct.absorber.generate_grid(mws, "Gold", matrix, step, t + th, t + th + t, name="circle_block")
    info["struct_name"] = (metal_sub_name, medium_sub_name, absorb_name)

    isComplete = c_modeler.solver.run(mws)

    if isComplete is not True:
        print("run failed")
        return

    # 返回 S 参数，对于单极化的吸收器来说，只需要一种 S参数的数据，SZmax(1),Zmax(1)
    sParam_Zmax1_Zmax1 = c_result.sParam.get_Zmax1_Zmax1(cst_file_path)
    sParam = {"Zmax1_Zmax1": sParam_Zmax1_Zmax1}
    info["sParam"] = sParam

    c_modeler.shape.delete_solid(mws, metal_sub_name[0], metal_sub_name[1])
    c_modeler.shape.delete_solid(mws, medium_sub_name[0], medium_sub_name[1])
    c_modeler.shape.delete_solid(mws, absorb_name[0], absorb_name[1])

    return info


# 单圆环
# r1 大半径    r2 小半径
def single_torus(mws, cst_file_path, n_size, r1, r2, t, th, step=1):
    info = {}

    struct_param = {"n_size": n_size, "r1": r1, "r2": r2, "t": t, "th": th}
    info["struct_param"] = struct_param

    matrix = m_struct.absorber.single_torus(n_size, r1, r2)

    info["matrix_data"] = (matrix,)

    c_modeler.material.load_material(mws, "Gold")
    c_modeler.material.load_material(mws, "PTFE (lossy)")

    c_modeler.solver.boundary(mws, Zmin="electric")

    metal_sub_name = c_struct.substrate.brick_sub(mws, "Gold", n_size, n_size, 0, t, step, name="metal_sub")
    medium_sub_name = c_struct.substrate.brick_sub(mws, "PTFE (lossy)", n_size, n_size, t, t + th, step,
                                                   name="medium_sub")
    absorb_name = c_struct.absorber.generate_grid(mws, "Gold", matrix, step, t + th, t + th + t, name="single_torus")
    info["struct_name"] = (metal_sub_name, medium_sub_name, absorb_name)

    isComplete = c_modeler.solver.run(mws)

    if isComplete is not True:
        print("run failed")
        return

    # 返回 S 参数，对于单极化的吸收器来说，只需要一种 S参数的数据，SZmax(1),Zmax(1)
    sParam_Zmax1_Zmax1 = c_result.sParam.get_Zmax1_Zmax1(cst_file_path)
    sParam = {"Zmax1_Zmax1": sParam_Zmax1_Zmax1}
    info["sParam"] = sParam

    c_modeler.shape.delete_solid(mws, metal_sub_name[0], metal_sub_name[1])
    c_modeler.shape.delete_solid(mws, medium_sub_name[0], medium_sub_name[1])
    c_modeler.shape.delete_solid(mws, absorb_name[0], absorb_name[1])

    return info


# 双圆环
# 外圆环：r1 大半径    r2 小半径
# 内圆环：r3 大半径    r4 小半径
def double_torus(mws, cst_file_path, n_size, r1, r2, r3, r4, t, th, step=1):
    info = {}

    struct_param = {"n_size": n_size, "r1": r1, "r2": r2, "r3": r3, "r4": r4, "t": t, "th": th}
    info["struct_param"] = struct_param

    matrix = m_struct.absorber.double_torus(n_size, r1, r2, r3, r4)

    info["matrix_data"] = (matrix,)

    c_modeler.material.load_material(mws, "Gold")
    c_modeler.material.load_material(mws, "PTFE (lossy)")

    c_modeler.solver.boundary(mws, Zmin="electric")

    metal_sub_name = c_struct.substrate.brick_sub(mws, "Gold", n_size, n_size, 0, t, step, name="metal_sub")
    medium_sub_name = c_struct.substrate.brick_sub(mws, "PTFE (lossy)", n_size, n_size, t, t + th, step,
                                                   name="medium_sub")
    absorb_name = c_struct.absorber.generate_grid(mws, "Gold", matrix, step, t + th, t + th + t, name="double_torus")
    info["struct_name"] = (metal_sub_name, medium_sub_name, absorb_name)

    isComplete = c_modeler.solver.run(mws)

    if isComplete is not True:
        print("run failed")
        return

    # 返回 S 参数，对于单极化的吸收器来说，只需要一种 S参数的数据，SZmax(1),Zmax(1)
    sParam_Zmax1_Zmax1 = c_result.sParam.get_Zmax1_Zmax1(cst_file_path)
    sParam = {"Zmax1_Zmax1": sParam_Zmax1_Zmax1}
    info["sParam"] = sParam

    c_modeler.shape.delete_solid(mws, metal_sub_name[0], metal_sub_name[1])
    c_modeler.shape.delete_solid(mws, medium_sub_name[0], medium_sub_name[1])
    c_modeler.shape.delete_solid(mws, absorb_name[0], absorb_name[1])

    return info


# 单开口圆环
# r1 大半径    r2 小半径
# proportion  开口占比  0 代表不开口    100 代表全开口即无图案 且该值必须为偶数
def open_single_ring(mws, cst_file_path, n_size, r1, r2, proportion, t, th, step=1):
    info = {}

    struct_param = {"n_size": n_size, "r1": r1, "r2": r2, "proportion": proportion, "t": t, "th": th}
    info["struct_param"] = struct_param

    matrix = m_struct.absorber.open_single_ring(n_size, r1, r2, proportion)

    info["matrix_data"] = (matrix,)

    c_modeler.material.load_material(mws, "Gold")
    c_modeler.material.load_material(mws, "PTFE (lossy)")

    c_modeler.solver.boundary(mws, Zmin="electric")

    metal_sub_name = c_struct.substrate.brick_sub(mws, "Gold", n_size, n_size, 0, t, step, name="metal_sub")
    medium_sub_name = c_struct.substrate.brick_sub(mws, "PTFE (lossy)", n_size, n_size, t, t + th, step,
                                                   name="medium_sub")
    absorb_name = c_struct.absorber.generate_grid(mws, "Gold", matrix, step, t + th, t + th + t,
                                                  name="open_single_ring")
    info["struct_name"] = (metal_sub_name, medium_sub_name, absorb_name)

    isComplete = c_modeler.solver.run(mws)

    if isComplete is not True:
        print("run failed")
        return

    # 返回 S 参数，对于单极化的吸收器来说，只需要一种 S参数的数据，SZmax(1),Zmax(1)
    sParam_Zmax1_Zmax1 = c_result.sParam.get_Zmax1_Zmax1(cst_file_path)
    sParam = {"Zmax1_Zmax1": sParam_Zmax1_Zmax1}
    info["sParam"] = sParam

    c_modeler.shape.delete_solid(mws, metal_sub_name[0], metal_sub_name[1])
    c_modeler.shape.delete_solid(mws, medium_sub_name[0], medium_sub_name[1])
    c_modeler.shape.delete_solid(mws, absorb_name[0], absorb_name[1])

    return info


# 十字混合
def cross_mixing(mws, cst_file_path, n_size, l, w, ag_step, filter_step, t, th, step=1):
    info = {}

    struct_param = {"n_size": n_size, "l": l, "w": w, "ag_step": ag_step, "filter_step": filter_step, "t": t, "th": th}
    info["struct_param"] = struct_param

    matrix = m_struct.absorber.cross_mixing(n_size, l, w, ag_step, filter_step)

    info["matrix_data"] = (matrix,)

    c_modeler.material.load_material(mws, "Gold")
    c_modeler.material.load_material(mws, "PTFE (lossy)")

    c_modeler.solver.boundary(mws, Zmin="electric")

    metal_sub_name = c_struct.substrate.brick_sub(mws, "Gold", n_size, n_size, 0, t, step, name="metal_sub")
    medium_sub_name = c_struct.substrate.brick_sub(mws, "PTFE (lossy)", n_size, n_size, t, t + th, step,
                                                   name="medium_sub")
    absorb_name = c_struct.absorber.generate_grid(mws, "Gold", matrix, step, t + th, t + th + t,
                                                  name="cross_mixing")
    info["struct_name"] = (metal_sub_name, medium_sub_name, absorb_name)

    isComplete = c_modeler.solver.run(mws)

    if isComplete is not True:
        print("run failed")
        return

    # 返回 S 参数，对于单极化的吸收器来说，只需要一种 S参数的数据，SZmax(1),Zmax(1)
    sParam_Zmax1_Zmax1 = c_result.sParam.get_Zmax1_Zmax1(cst_file_path)
    sParam = {"Zmax1_Zmax1": sParam_Zmax1_Zmax1}
    info["sParam"] = sParam

    c_modeler.shape.delete_solid(mws, metal_sub_name[0], metal_sub_name[1])
    c_modeler.shape.delete_solid(mws, medium_sub_name[0], medium_sub_name[1])
    c_modeler.shape.delete_solid(mws, absorb_name[0], absorb_name[1])

    return info


# 空十字生长
def cross_like(mws, cst_file_path, n_size, l, w, ag_step, filter_step, t, th, step=1):
    info = {}

    struct_param = {"n_size": n_size, "l": l, "w": w, "ag_step": ag_step, "filter_step": filter_step, "t": t, "th": th}
    info["struct_param"] = struct_param

    matrix = m_struct.absorber.cross_like(n_size, l, w, ag_step, filter_step)

    info["matrix_data"] = (matrix,)

    c_modeler.material.load_material(mws, "Gold")
    c_modeler.material.load_material(mws, "PTFE (lossy)")

    c_modeler.solver.boundary(mws, Zmin="electric")

    metal_sub_name = c_struct.substrate.brick_sub(mws, "Gold", n_size, n_size, 0, t, step, name="metal_sub")
    medium_sub_name = c_struct.substrate.brick_sub(mws, "PTFE (lossy)", n_size, n_size, t, t + th, step,
                                                   name="medium_sub")
    absorb_name = c_struct.absorber.generate_grid(mws, "Gold", matrix, step, t + th, t + th + t,
                                                  name="cross_like")
    info["struct_name"] = (metal_sub_name, medium_sub_name, absorb_name)

    isComplete = c_modeler.solver.run(mws)

    if isComplete is not True:
        print("run failed")
        return

    # 返回 S 参数，对于单极化的吸收器来说，只需要一种 S参数的数据，SZmax(1),Zmax(1)
    sParam_Zmax1_Zmax1 = c_result.sParam.get_Zmax1_Zmax1(cst_file_path)
    sParam = {"Zmax1_Zmax1": sParam_Zmax1_Zmax1}
    info["sParam"] = sParam

    c_modeler.shape.delete_solid(mws, metal_sub_name[0], metal_sub_name[1])
    c_modeler.shape.delete_solid(mws, medium_sub_name[0], medium_sub_name[1])
    c_modeler.shape.delete_solid(mws, absorb_name[0], absorb_name[1])

    return info
