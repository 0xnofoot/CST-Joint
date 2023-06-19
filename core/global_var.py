import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

# CST的python库路径，自己按照CST安装路径修改
CST_HOME = r"D:\CST\AMD64\python_cst_libraries"

WORK_HOME = rootPath

cst_save_dir = os.path.join(WORK_HOME, "CST_Project")
output_dir = os.path.join(WORK_HOME, "output")
resource_dir = os.path.join(WORK_HOME, "resource")
data_dir = os.path.join(WORK_HOME, "data")
