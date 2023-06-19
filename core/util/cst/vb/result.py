import sys

import core.global_var

CST_HOME = core.global_var.CST_HOME

# 导入CST软件Python支持包 自行修改路径
sys.path.append(CST_HOME)
import cst.results as result


def get_sParameters(file_path, sParam, allow_interactive):
    project = result.ProjectFile(file_path, allow_interactive)
    sParam = "1D Results\\S-Parameters\\" + sParam
    sParam_data = project.get_3d().get_result_item(sParam)
    data = sParam_data.get_data()
    return data
