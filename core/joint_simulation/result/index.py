import os

from core import global_var

output_dir = global_var.output_dir


# index 数据保存
# 记得写 index 格式标准！！！！！
# 记得写 batch
def save(batch, index, struct_name, struct_param, dir_project="default_Project"):
    index_save_dir = os.path.join(output_dir, dir_project, "index")
    if not os.path.exists(index_save_dir):
        os.makedirs(index_save_dir)
    index_file_path = os.path.join(index_save_dir, "index.txt")
    with open(index_file_path, mode="a", encoding="utf-8") as f:
        line = str(index) + "\t" + str(batch) + "\t" + str(struct_name) + "\t" + str(struct_param) + "\n"
        f.write(line)

    batch_index_file_path = os.path.join(index_save_dir, str(batch) + "_index.txt")
    with open(batch_index_file_path, mode="a", encoding="utf-8") as f:
        line = str(index) + "\t" + str(batch) + "\t" + str(struct_name) + "\t" + str(struct_param) + "\n"
        f.write(line)
