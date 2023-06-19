import os
import shutil
import global_var

data_base_dir = os.path.join(global_var.data_dir, "absorber", "cross_mixing")
index_file = os.path.join(data_base_dir, "index", "index.txt")

sParam_dir = os.path.join(data_base_dir, "data", "cst", "sParam", "Zmax1_Zmax1")
md_dir = os.path.join(data_base_dir, "data", "matrix", "data", "layer_1")
mp_dir = os.path.join(data_base_dir, "data", "matrix", "pic", "layer_1")

with open(index_file, "r", encoding="utf-8") as f:
    lines = f.readlines()
    count = 1
    for line in lines:
        if "{'n_size': 64, 'l': 40, 'w': 10," in line:
            bl = line.split("\t")
            index = bl[0]
            bl[0] = str(count)
            bl[1] = str(int(count - 1) // 100 + 1)

            line = str.join("\t", bl)
            with open(os.path.join("cross_mixing_param5-15-16", "index", "index.txt"), mode="a",
                      encoding="utf-8") as inf:
                inf.write(line)

            sFile = os.path.join(sParam_dir, index + "_Zmax1_Zmax1.txt")
            mdFile = os.path.join(md_dir, index + "_mat_data.txt")
            mpFile = os.path.join(mp_dir, index + "_mat_pic.png")

            shutil.copy(sFile, os.path.join("cross_mixing_param5-15-16", "data", "s", str(count) + "_Zmax1_Zmax1.txt"))
            shutil.copy(mdFile, os.path.join("cross_mixing_param5-15-16", "data", "md", str(count) + "_mat_data.txt"))
            shutil.copy(mpFile, os.path.join("cross_mixing_param5-15-16", "data", "mp", str(count) + "_mat_pic.png"))

            count += 1
