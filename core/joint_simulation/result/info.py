from core.joint_simulation.result import index as j_index, matrix as j_matrix, sParam as j_sParam


# info 处理函数
def handle_by_layer(batch, index, info, layer, dir_project, mtype="default"):
    print("log-batch: " + str(batch) + " index: " + str(index))

    # index 数据保存
    struct_name = info["struct_name"]
    struct_param = info["struct_param"]
    j_index.save(batch, index, struct_name, struct_param, dir_project=dir_project)

    # 按层保存矩阵图像和数据
    mats = info["matrix_data"]
    j_matrix.save_pic_by_layer(batch, mats, layer=layer, dir_project=dir_project, prefix=str(index))
    j_matrix.save_data_by_layer(batch, mats, layer=layer, dir_project=dir_project, prefix=str(index))

    sParam_data = info["sParam"]

    if mtype is "default":
        j_sParam.save_all_Zmaxin(batch, sParam_data, dir_project=dir_project, prefix=str(index))
    elif mtype is "AT":
        j_sParam.save_AT(batch, sParam_data, dir_project=dir_project, prefix=str(index))
    elif mtype is "absorber":
        j_sParam.save_sParam_by_name("Zmax1_Zmax1", batch, sParam_data, dir_project=dir_project, prefix=str(index))
