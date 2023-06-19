import os
import re

from core import global_var

output_dir = global_var.output_dir


# 按照格式保存 S参数
# S 参数格式为 [(frequency, (real part, imaginary part)), ------]
# 格式上是一个列表， 每个元素是一个元组，元组内有频率，实部和虚部的信息
# 格式处理后按照 频率 实部 虚部 按行写入文件， 以 space 分割
def save(sPara_data, dir, file_name):
    save_dir = os.path.join(output_dir, dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    file_path = os.path.join(save_dir, file_name)
    with open(file_path, mode="a", encoding="utf-8") as f:
        for i in range(len(sPara_data)):
            line = str(sPara_data[i]).replace("(", "").replace(")", "")
            line = line + "\n"
            pattern = re.compile(r"[+-][\d.]+j")
            find_str = str(pattern.findall(line)[0])
            line = re.sub(pattern, " " + find_str, line)
            line = line.replace("j", "").replace(", ", " ")
            f.write(line)


def save_sParam_by_name(sName, batch, sParam, dir_project="default_Project", prefix="", suffix=".txt"):
    save_dir_base = os.path.join(dir_project, str(batch) + "_batch", "cst", "sParam")
    save(sParam[sName], os.path.join(save_dir_base, sName), prefix + "_" + sName + suffix)


def save_all_Zmaxin(batch, sParam, dir_project="default_Project", prefix="", suffix=".txt"):
    save_dir_base = os.path.join(dir_project, str(batch) + "_batch", "cst", "sParam")

    Z = "Zmax1_Zmax1"
    save(sParam[Z], os.path.join(save_dir_base, Z), prefix + "_" + Z + suffix)

    Z = "Zmax2_Zmax1"
    save(sParam[Z], os.path.join(save_dir_base, Z), prefix + "_" + Z + suffix)

    Z = "Zmin1_Zmax1"
    save(sParam[Z], os.path.join(save_dir_base, Z), prefix + "_" + Z + suffix)

    Z = "Zmin2_Zmax1"
    save(sParam[Z], os.path.join(save_dir_base, Z), prefix + "_" + Z + suffix)

    Z = "Zmax1_Zmax2"
    save(sParam[Z], os.path.join(save_dir_base, Z), prefix + "_" + Z + suffix)

    Z = "Zmax2_Zmax2"
    save(sParam[Z], os.path.join(save_dir_base, Z), prefix + "_" + Z + suffix)

    Z = "Zmin1_Zmax2"
    save(sParam[Z], os.path.join(save_dir_base, Z), prefix + "_" + Z + suffix)

    Z = "Zmin2_Zmax2"
    save(sParam[Z], os.path.join(save_dir_base, Z), prefix + "_" + Z + suffix)


# 保存 AT 所需要的 S参数
def save_AT(batch, sParam, dir_project="AT", prefix="", suffix=".txt"):
    save_dir_base = os.path.join(dir_project, str(batch) + "_batch", "cst", "sParam")

    Z = "Zmin2_Zmax1"
    save(sParam[Z], os.path.join(save_dir_base, Z), prefix + "_" + Z + suffix)

    Z = "Zmin1_Zmax1"
    save(sParam[Z], os.path.join(save_dir_base, Z), prefix + "_" + Z + suffix)

    Z = "Zmin2_Zmax2"
    save(sParam[Z], os.path.join(save_dir_base, Z), prefix + "_" + Z + suffix)

    Z = "Zmin1_Zmax2"
    save(sParam[Z], os.path.join(save_dir_base, Z), prefix + "_" + Z + suffix)
