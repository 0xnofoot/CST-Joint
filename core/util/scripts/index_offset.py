import os

data_dir = "cross_mixing_test"
offset = 11

sParam_dir = os.path.join(data_dir, "data", "cst", "sParam", "Zmax1_Zmax1")
mData_dir = os.path.join(data_dir, "data", "matrix", "data", "layer_1")
mPic_dir = os.path.join(data_dir, "data", "matrix", "pic", "layer_1")

sFiles = reversed(os.listdir(sParam_dir))
for sFile in sFiles:
    index = sFile.split("_")[0]
    new_index = int(index) + offset * 100
    print(index + "--->" + str(new_index))

    new_sFile = str(new_index) + "_Zmax1_Zmax1.txt"
    sFile = os.path.join(sParam_dir, sFile)
    new_sFile = os.path.join(sParam_dir, new_sFile)
    os.rename(sFile, new_sFile)

print("/////////////////////////")

mdFiles = reversed(os.listdir(mData_dir))
for mdFile in mdFiles:
    index = mdFile.split("_")[0]
    new_index = int(index) + offset * 100
    print(index + "--->" + str(new_index))

    new_mdFile = str(new_index) + "_mat_data.txt"
    mdFile = os.path.join(mData_dir, mdFile)
    new_mdFile = os.path.join(mData_dir, new_mdFile)
    os.rename(mdFile, new_mdFile)

print("/////////////////////////")

mpFiles = reversed(os.listdir(mPic_dir))
for mpFile in mpFiles:
    index = mpFile.split("_")[0]
    new_index = int(index) + offset * 100
    print(index + "--->" + str(new_index))

    new_mpFile = str(new_index) + "_mat_pic.png"
    mpFile = os.path.join(mPic_dir, mpFile)
    new_mpFile = os.path.join(mPic_dir, new_mpFile)
    os.rename(mpFile, new_mpFile)

index_dir = os.path.join(data_dir, "index")
index_file_path = os.path.join(index_dir, "index.txt")
new_index_file_path = os.path.join(index_dir, "new_index.txt")

new_lines_buff = []
with open(index_file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        index = line.split("\t")[0]
        batch = line.split("\t")[1]
        tail = line.split("\t")[2:]
        new_index = str(int(index) + offset * 100)
        new_batch = str(int(batch) + offset)
        tail.insert(0, new_batch)
        tail.insert(0, new_index)
        new_lines_buff.append("\t".join(tail))

print(new_lines_buff[0])
with open(new_index_file_path, "w") as file:
    for line in new_lines_buff:
        file.write(line)
