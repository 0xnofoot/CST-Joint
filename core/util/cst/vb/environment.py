import sys
import os

import core.global_var

CST_HOME = core.global_var.CST_HOME
cst_save_dir = core.global_var.cst_save_dir

# 导入CST软件Python支持包 自行修改路径
sys.path.append(CST_HOME)
import cst.interface


# 创建CST MicroWave Studio工作环境和 modeler接口 保存工程文件
# return cst_env的目的是保证其不会被gc，因为mws的一些接口是靠进程与 cst_env连接
# 如果cst_env被 gc， 那 mws的一些函数会失效，比如 save()函数
# 不得不说这个bug很sb，而且官方文档里半句没提
def create_new_mws(name, dir_project):
    name = name + ".cst"
    if dir_project is None:
        dir_project = name
    if not os.path.exists(cst_save_dir):
        os.makedirs(cst_save_dir)
    cst_file_path = os.path.join(cst_save_dir, dir_project, name)
    cst_env = cst.interface.DesignEnvironment()
    mws = cst_env.new_mws()
    mws.save(cst_file_path)
    return cst_env, mws, cst_file_path
