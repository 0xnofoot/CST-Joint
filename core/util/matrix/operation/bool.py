# 矩阵加法
# 适用于 float 数据类型 的矩阵
# 如果不是 float 请提前转换
def add(matrix1, *matrix2):
    for matrix in matrix2:
        matrix1 = matrix1 + matrix
        matrix1[matrix1 > 1] = 1
    return matrix1


# 矩阵减法
# 适用于 float 数据类型 的矩阵
# 如果不是 float 请提前转换
def subtract(matrix1, *matrix2):
    for matrix in matrix2:
        matrix1 = matrix1 - matrix
        matrix1[matrix1 < 0] = 0
    return matrix1
