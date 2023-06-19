from core.util.cst.vb import environment
from core.util.cst.vb import modeler


# 创建一个MWS工程并初始化
def create_new_mws_project(name, template_file_name, freq_low, freq_high, dir_project=None):
    cst_env, mws, cst_file_path = environment.create_new_mws(name, dir_project)
    modeler.initial_template(mws.modeler, template_file_name, freq_low, freq_high)
    return cst_env, mws, cst_file_path
