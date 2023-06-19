from core.joint_simulation import single
from core.util.cst import modeler as c_modeler
from core.joint_simulation import result as j_result


def dorr(file_name, batch=1, dir_project="AT", freq_low=0.2, freq_high=2, isStart=True, cst_object=None):
    if isStart is True:
        cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
            file_name, "template_unit_cell", freq_low, freq_high, dir_project)
        cst_object = (cst_env, mws, cst_file_path)
    else:
        cst_env, mws, cst_file_path = cst_object

    # 增加 Zmin 入射端口
    # 被注释掉的原因是非对称传输一个端口的数据已经足够
    # 增加一个端口只会增加仿真时间
    # 在 S 参数的处理中，所有关于 Zmin 端口的入射数据的操作也都被注释掉了
    # c_modeler.solver.add_port(mws, "Zmin")

    if dir_project is None:
        dir_project = file_name
    # n_size: 64
    # l: 48~57, 因为 l必须为偶数，所以总共 5 组数据, 分别为 48, 50 52，54，56
    # w: 6~11, 5 组数据，分别为 6， 7， 8， 9， 10
    # g: 5~20, 15 组数据
    # s: 5~20, 15 组数据
    # 每一个批次仿真 15x15 共225组数据
    # 将 l 和 w 给定，仿真所有的 g 和 s， 所以是 225 组

    n_size = 64
    l = int((batch - 1) % 5) * 2 + 48
    w = int((batch - 1) / 5) + 6
    index = int(batch - 1) * 225

    for g in range(5, 20):
        for s in range(5, 20):
            # ！！！: 返回的 info 标准：
            # info 是一个信息字典， 用于返回这一次仿真中所有的数据信息
            # 其中包括
            # info["struct_param"] : 结构参数信息， 结构参数本身也是一个字典
            # info["matrix_data"]     : 矩阵数据信息，是一个元组，因为可能有多层矩阵
            # info["struct_name"]  : 结构器件和名称信息，是一个元组
            # info["sParam"]       : S 参数数据信息，是一个字典
            index = index + 1
            info = single.AT.dorr(mws, cst_file_path, n_size, l, w, g, s)
            j_result.info.handle_by_layer(batch, index, info, layer=2, dir_project=dir_project, mtype="AT")

    return cst_object
