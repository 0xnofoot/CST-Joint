import numpy as np


# 获取矩阵中 每一个块周围八个块的数据信息
def get_round_bricks(n_size, brick):
    x = brick[0]
    y = brick[1]
    round_bricks = list()
    round_bricks.append((x - 1, y - 1))
    round_bricks.append((x - 1, y))
    round_bricks.append((x - 1, y + 1))
    round_bricks.append((x, y - 1))
    round_bricks.append((x, y + 1))
    round_bricks.append((x + 1, y - 1))
    round_bricks.append((x + 1, y))
    round_bricks.append((x + 1, y + 1))

    def limit_filter(brick):
        if 0 <= brick[0] < n_size and 0 <= brick[1] < n_size:
            return True
        return False

    round_bricks = list(filter(lambda b: limit_filter(b), round_bricks))

    return round_bricks


# 环绕生长，用于生成聚合度高的矩阵数据
def around_growth(n_size, count, step, ac_brick_initial=None):
    matrix = np.zeros((n_size, n_size))
    ac_count = count
    ac_bricks = set()
    iac_bricks = set()

    if ac_brick_initial is None:
        # ac_brick_initial = (np.random.randint(0, n_size), np.random.randint(0, n_size))
        ac_brick_initial = (int(n_size / 2), int(n_size / 2))

    matrix[ac_brick_initial] = 1

    ac_bricks.add(ac_brick_initial)

    def active_brick():
        if len(ac_bricks) != 0:
            ac_brick = ac_bricks.pop()
        else:
            ac_brick = iac_bricks.pop()
        iac_bricks.add(ac_brick)

        round_bricks = get_round_bricks(n_size, ac_brick)

        def ac_filter(brick):
            if brick not in ac_bricks and brick not in iac_bricks:
                return True
            return False

        round_bricks = list(filter(lambda b: ac_filter(b), round_bricks))
        np.random.shuffle(round_bricks)
        if len(round_bricks) < ac_count:
            n = len(round_bricks)
        else:
            n = ac_count
        round_bricks = round_bricks[:n]

        return round_bricks

    for i in range(step):
        ac_round_bricks = active_brick()
        for b in ac_round_bricks:
            matrix[b] = 1
            ac_bricks.add(b)

    return matrix


# 矩阵过滤
def filter_by_around(n_size, matrix, step=1):
    for i in range(step):
        for brick, value in np.ndenumerate(matrix):
            round_bricks = get_round_bricks(n_size, brick)
            round_sum = sum(map(lambda b: matrix[b], round_bricks))

            if len(round_bricks) == 3 and round_sum >= 2:
                matrix[brick] = 1
                continue
            elif len(round_bricks) == 5 and round_sum >= 3:
                matrix[brick] = 1
                continue

            if value == 0 and round_sum >= 5:
                matrix[brick] = 1
            elif value == 1 and round_sum < 4:
                matrix[brick] = 0

    return matrix
