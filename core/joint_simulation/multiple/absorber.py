import os.path

from core.joint_simulation import single
from core.util.cst import modeler as c_modeler
from core.joint_simulation import result as j_result


# 实际上在这个文件中存在大量重复的代码
# 主要是最早设计时的遗漏导致
# 很多时候换个工程实际上就是换个调用函数而已, 甚至传入的参数都是一样( mixing 和 like 函数最为典型)
# 如果可以，使用函数式编程重构这个文件，还有 single 中的文件
# 代码有效率会提升很多


# ！！！: 返回的 info 标准：
# info 是一个信息字典， 用于返回这一次仿真中所有的数据信息
# 其中包括
# info["struct_param"] : 结构参数信息， 结构参数本身也是一个字典
# info["matrix_data"]     : 矩阵数据信息，是一个元组，因为可能有多层矩阵
# info["struct_name"]  : 结构的器件和名称信息，是一个元组
# info["sParam"]       : S 参数数据信息，是一个字典


# 竖条
# 在同一个 CST 文件中仿真，时间越久会越慢， 在竖条和十字的代码中没对这个问题优化
def vertical_bar(file_name, batch=1, dir_project="absorber", freq_low=1, freq_high=5, isStart=True, cst_object=None):
    if isStart is True:
        cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
            file_name, "template_unit_cell", freq_low, freq_high, dir_project)
        cst_object = (cst_env, mws, cst_file_path)
    else:
        cst_env, mws, cst_file_path = cst_object

    # n_size: 64
    # 数据量较少 不用分batch
    # l/2: 8~31,
    # w/2: 2~8,

    n_size = 64
    t = 0.58
    th = 2.4
    index = 159

    for w2 in range(2, 9):
        for l2 in range(8, 32):
            l = l2 * 2
            w = w2 * 2
            index = index + 1
            info = single.absorber.vertical_bar(mws, cst_file_path, n_size, l, w, t, th)
            j_result.info.handle_by_layer(batch, index, info, layer=1, dir_project=os.path.join(dir_project, file_name),
                                          mtype="absorber")

    return cst_object


# 十字
def cross(file_name, batch=1, dir_project="absorber", freq_low=1, freq_high=5):
    cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
        file_name, "template_unit_cell", freq_low, freq_high, dir_project)

    # n_size: 64
    # 数据量较少 不用分batch
    # l/2: 9~31,
    # w/2: l/2 * 0.25 ~ l/2 * 0.75,

    n_size = 64
    t = 0.58
    th = 2.4
    index = 0

    for l2 in range(9, 32):
        w2_start = int(l2 * 0.25)
        w2_stop = int(l2 * 0.75)
        for w2 in range(w2_start, w2_stop + 1):
            l = l2 * 2
            w = w2 * 2
            index = index + 1
            if index % 10 == 0:
                cst_env.close()
                cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
                    file_name, "template_unit_cell", freq_low, freq_high, dir_project)
            info = single.absorber.cross(mws, cst_file_path, n_size, l, w, t, th)
            j_result.info.handle_by_layer(batch, index, info, layer=1, dir_project=os.path.join(dir_project, file_name),
                                          mtype="absorber")


# 耶路撒冷十字
def jerusalem_cross(file_name, batch=1, dir_project="absorber", freq_low=1, freq_high=5):
    cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
        file_name, "template_unit_cell", freq_low, freq_high, dir_project)

    # n_size: 64
    # l/2: 8~24,
    # w/2: 2~8,
    # el/2: 4~18,
    # ew: 2~6,

    n_size = 64
    t = 0.58
    th = 2.4
    index = 0

    for l2 in range(8, 24):
        for w2 in range(2, 8):
            for el2 in range(4, 18):
                for ew in range(2, 6):
                    l = l2 * 2
                    w = w2 * 2
                    el = el2 * 2

                    index = index + 1
                    if index < 4827:
                        continue

                    if index % 5 == 0:
                        cst_env.close()
                        cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
                            file_name, "template_unit_cell", freq_low, freq_high, dir_project)

                    info = single.absorber.jerusalem_cross(mws, cst_file_path, n_size, l, w, el, ew, t, th)
                    j_result.info.handle_by_layer(batch, index, info, layer=1,
                                                  dir_project=os.path.join(dir_project, file_name),
                                                  mtype="absorber")


# 由于 CST 存在同一文件联仿时, 时间越长仿真越慢的问题
# 所以在方环的代码中修改了之前的逻辑
# 每十个 index 关闭当前工程并重新打开一个新的工程文件
def square_ring(file_name, batch=1, dir_project="absorber", freq_low=1, freq_high=5):
    cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
        file_name, "template_unit_cell", freq_low, freq_high, dir_project)

    # n_size: 64
    # l/2: 8~31,
    # w: 视 l 的变化而变化， l 越大 w 的取值越多
    # l  l * 0.5     l * 0.5 * 0.25   l * 0.5 * 0.75         w
    # 16   8              2                6                2~6
    # 40   20             5                15               5~15
    # 60   30             7                22               7~22
    # 62   31             7                23               7~23

    n_size = 64
    t = 0.58
    th = 2.4
    index = 0

    for l2 in range(8, 32):
        l = l2 * 2
        w_start = int(l * 0.5 * 0.25)
        w_stop = int(l * 0.5 * 0.75)
        for w in range(w_start, w_stop + 1):
            index = index + 1
            if index % 3 == 0:
                cst_env.close()
                cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
                    file_name, "template_unit_cell", freq_low, freq_high, dir_project)

            info = single.absorber.square_ring(mws, cst_file_path, n_size, l, w, t, th)
            j_result.info.handle_by_layer(batch, index, info, layer=1, dir_project=os.path.join(dir_project, file_name),
                                          mtype="absorber")


# 单开口方环
def single_split_square_ring(file_name, batch=1, dir_project="absorber", freq_low=1, freq_high=5):
    cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
        file_name, "template_unit_cell", freq_low, freq_high, dir_project)

    # n_size: 64
    # l 和 w 的取值和方环相同
    # e 和 x 的取值标准:
    # e + x <= l - w * 2

    n_size = 64
    t = 0.58
    th = 2.4
    index = 0

    for l2 in range(8, 32):
        l = l2 * 2
        w_start = int(l * 0.5 * 0.25)
        w_stop = int(l * 0.5 * 0.75)
        for w in range(w_start, w_stop + 1):
            x2_start = int((l - w * 2) * 0.05)
            x2_stop = int((l - w * 2) * 0.25)

            for x2 in range(x2_start + 1, x2_stop + 1):
                x = x2 * 2
                e_level_1 = int((l - w * 2) * 0.25) - x2
                e_level_2 = int((l - w * 2) * 0.5) - x2
                e_level_3 = int((l - w * 2) * 0.75) - x2

                for e in (e_level_1, e_level_2, e_level_3):
                    index = index + 1
                    if index % 5 == 0:
                        cst_env.close()
                        cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
                            file_name, "template_unit_cell", freq_low, freq_high, dir_project)

                    info = single.absorber.single_split_square_ring(mws, cst_file_path, n_size, l, w, e, x, t, th)
                    j_result.info.handle_by_layer(batch, index, info, layer=1,
                                                  dir_project=os.path.join(dir_project, file_name),
                                                  mtype="absorber")


# 圆形块
# 每两个重新打开
def circle_block(file_name, batch=1, dir_project="absorber", freq_low=1, freq_high=5):
    cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
        file_name, "template_unit_cell", freq_low, freq_high, dir_project)

    # n_size: 64
    # 数据量较少 不用分batch
    # r: 2 ~ 31

    n_size = 64
    t = 0.58
    th = 2.4
    index = 0

    for r in range(2, 32):
        index = index + 1
        if index % 2 == 0:
            cst_env.close()
            cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
                file_name, "template_unit_cell", freq_low, freq_high, dir_project)

        info = single.absorber.circle_block(mws, cst_file_path, n_size, r, t, th)
        j_result.info.handle_by_layer(batch, index, info, layer=1, dir_project=os.path.join(dir_project, file_name),
                                      mtype="absorber")


# 单圆环
# r1 大半径    r2 小半径
# 每两个重新打开
def single_torus(file_name, batch=1, dir_project="absorber", freq_low=1, freq_high=5):
    cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
        file_name, "template_unit_cell", freq_low, freq_high, dir_project)

    # n_size: 64
    # r1: 2 ~ 31
    # r2: r1 * 0.2 ~ r1 * 0.8

    n_size = 64
    t = 0.58
    th = 2.4
    index = 0

    for r1 in range(2, 32):
        r2_start = int(r1 * 0.2)
        r2_stop = int(r1 * 0.8)
        if r2_start == 0:
            r2_start = 1

        for r2 in range(r2_start, r2_stop + 1):
            index = index + 1
            if index % 2 == 0:
                cst_env.close()
                cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
                    file_name, "template_unit_cell", freq_low, freq_high, dir_project)

            info = single.absorber.single_torus(mws, cst_file_path, n_size, r1, r2, t, th)
            j_result.info.handle_by_layer(batch, index, info, layer=1, dir_project=os.path.join(dir_project, file_name),
                                          mtype="absorber")


# 双圆环
# 外圆环：r1 大半径    r2 小半径
# 内圆环：r3 大半径    r4 小半径
def double_torus(file_name, batch=1, dir_project="absorber", freq_low=1, freq_high=5):
    cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
        file_name, "template_unit_cell", freq_low, freq_high, dir_project)

    # n_size: 64
    # r1: 24 ~ 31
    # r2: r1 * 0.5 ~ r1 * 0.8
    # r3: 8 ~ r2 * 0.8
    # r4: r3 * 0.4 ~ r3 * 0.8

    n_size = 64
    t = 0.58
    th = 2.4
    index = 0

    for r1 in range(24, 32):
        r2_start = int(r1 * 0.5)
        r2_stop = int(r1 * 0.8)

        for r2 in range(r2_start, r2_stop + 1):
            r3_stop = int(r2 * 0.8)

            for r3 in range(8, r3_stop + 1):
                r4_start = int(r3 * 0.4)
                r4_stop = int(r3 * 0.8)
                for r4 in range(r4_start, r4_stop + 1):
                    index = index + 1
                    if index < 1869:
                        continue
                    if index % 5 == 0:
                        cst_env.close()
                        cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
                            file_name, "template_unit_cell", freq_low, freq_high, dir_project)

                    info = single.absorber.double_torus(mws, cst_file_path, n_size, r1, r2, r3, r4, t, th)
                    j_result.info.handle_by_layer(batch, index, info, layer=1,
                                                  dir_project=os.path.join(dir_project, file_name),
                                                  mtype="absorber")


# 单开口圆环
# r1 大半径    r2 小半径
# proportion  开口占比  0 代表不开口    100 代表全开口即无图案 且该值必须为偶数
def open_single_ring(file_name, batch=1, dir_project="absorber", freq_low=1, freq_high=5):
    cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
        file_name, "template_unit_cell", freq_low, freq_high, dir_project)

    # n_size: 64
    # r1: 8 ~ 31
    # r2: r1 * 0.3 ~ r1 * 0.7
    # proportion / 2: 4 ~ 10

    n_size = 64
    t = 0.58
    th = 2.4
    index = 0

    for r1 in range(8, 32):
        r2_start = int(r1 * 0.3)
        r2_stop = int(r1 * 0.7)
        if r2_start == 0:
            r2_start = 1

        for r2 in range(r2_start, r2_stop + 1):

            for proportion2 in range(4, 11):
                proportion = proportion2 * 2
                index = index + 1
                if index % 2 == 0:
                    cst_env.close()
                    cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
                        file_name, "template_unit_cell", freq_low, freq_high, dir_project)

                info = single.absorber.open_single_ring(mws, cst_file_path, n_size, r1, r2, proportion, t, th)
                j_result.info.handle_by_layer(batch, index, info, layer=1,
                                              dir_project=os.path.join(dir_project, file_name),
                                              mtype="absorber")


# 十字混合
# param 参数列表：用于外部传入参数
# 混合模型不适合一次性跑完
def cross_mixing(file_name, param, batch=1, dir_project="absorber", freq_low=1, freq_high=5):
    cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
        file_name, "template_unit_cell", freq_low, freq_high, dir_project)

    # n_size: 64

    n_size = 64
    t = 0.58
    th = 2.4
    index_start = (batch - 1) * 100
    index_stop = batch * 100

    l = param[0]
    w = param[1]
    ag_step = param[2]
    filter_step = param[3]

    for index in range(index_start, index_stop):
        index = index + 1
        if index % 5 == 0:
            cst_env.close()
            cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
                file_name, "template_unit_cell", freq_low, freq_high, dir_project)

        info = single.absorber.cross_mixing(mws, cst_file_path, n_size, l, w, ag_step, filter_step, t, th)
        j_result.info.handle_by_layer(batch, index, info, layer=1,
                                      dir_project=os.path.join(dir_project, file_name),
                                      mtype="absorber")

    cst_env.close()


# 空十字生长
# param 参数列表：用于外部传入参数
# 混合模型不适合一次性跑完
def cross_like(file_name, param, batch=1, dir_project="absorber", freq_low=1, freq_high=5):
    cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
        file_name, "template_unit_cell", freq_low, freq_high, dir_project)

    # n_size: 64

    n_size = 64
    t = 0.58
    th = 2.4
    index_start = (batch - 1) * 100
    index_stop = batch * 100

    l = param[0]
    w = param[1]
    ag_step = param[2]
    filter_step = param[3]

    for index in range(index_start, index_stop):
        index = index + 1
        if index % 5 == 0:
            cst_env.close()
            cst_env, mws, cst_file_path = c_modeler.initial.create_new_mws_project(
                file_name, "template_unit_cell", freq_low, freq_high, dir_project)

        info = single.absorber.cross_like(mws, cst_file_path, n_size, l, w, ag_step, filter_step, t, th)
        j_result.info.handle_by_layer(batch, index, info, layer=1,
                                      dir_project=os.path.join(dir_project, file_name),
                                      mtype="absorber")

    cst_env.close()
