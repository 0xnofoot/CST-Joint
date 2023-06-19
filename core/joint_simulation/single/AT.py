from core.util.matrix import struct as m_struct
from core.util.cst import modeler as c_modeler, struct as c_struct, result as c_result


# ！！！: 返回的 info 标准：
# info 是一个信息字典， 用于返回这一次仿真中所有的数据信息
# 其中包括
# info["struct_param"] : 结构参数信息， 结构参数本身也是一个字典
# info["matrix_data"]     : 矩阵数据信息，是一个元组，因为可能有多层矩阵
# info["struct_name"]  : 结构器件和名称信息，是一个元组
# info["sParam"]       : S 参数数据信息，是一个字典
def dorr(mws, cst_file_path, n_size, l, w, g, s, th=20, t=0.2, step=2):
    info = {}

    struct_param = {"n_size": n_size, "l": l, "w": w, "g": g, "s": s, "th": th, "t": t}
    info["struct_param"] = struct_param

    dorr_mat_up, dorr_mat_down = m_struct.AT.dorr(n_size, l, w, g, s)
    info["matrix_data"] = (dorr_mat_up, dorr_mat_down)

    # c_modeler.material.define_material(mws, "Polyimide", 3.0, 1.0, 0.008, color=(0.89, 1, 0.9569))
    c_modeler.material.load_material(mws, "Aluminum")
    c_modeler.material.load_material(mws, "Polyimide (lossy)")
    sub_name = c_struct.substrate.brick_sub(mws, "Polyimide (lossy)", n_size, n_size, 0, th, step)
    dorr_name = c_struct.AT.dorr(mws, "Aluminum", l, w, g, s, th, t, step)
    info["struct_name"] = (sub_name, dorr_name)

    isComplete = c_modeler.solver.run(mws)

    if isComplete is not True:
        print("run failed")
        return

    # 返回 AT 的 S参数， 总共8个数据， 保存在一个字典里
    # 由于已经删除了 Zmin 端口的入射数据
    # 所以该字典中只包含 Zmax 的入射数据
    sParam = c_result.sParam.get_all_Zmaxin(cst_file_path)
    info["sParam"] = sParam

    c_modeler.shape.delete_solid(mws, sub_name[0], sub_name[1])
    c_modeler.shape.delete_solid(mws, dorr_name[0], dorr_name[1])

    return info
