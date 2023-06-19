import time
import psutil

# CST 的进程监测函数
# 由于 CST 官方提供的 Python 代码库存在 bug
# 调用 CST 环境的关闭函数时有一定的概率关闭失败，程序会卡在关闭函数中
# 因此调用这个监测函数可以监测某个 CST 进程存活的时间
# 通过判断存活时间是否正常来对其进行关闭
# 需要注意的是，如果以开启新线程调用这个函数，CST 在进行仿真计算时会阻塞这个函数
# 因此请单独以脚本的形式启动这个文件即可
# 这个函数可以同时监测多个 CST 进程，因此在启动多个实例时请确保只运行一次这个脚本


CST_KEYWORD = "cst design environment"
PROCESS_TIMEOUT = 3200  # 进程超时时间，单位为秒

while True:
    processes = psutil.process_iter()
    filtered_processes = [p for p in processes if "cst design environment" in p.name().lower()]
    for proc in filtered_processes:
        uptime = time.time() - proc.create_time()
        print(f"pid={proc.pid}, uptime={uptime:.2f}s")
        if uptime > PROCESS_TIMEOUT:
            print(f"Killing process: pid={proc.pid}, uptime={uptime:.2f}s")
            proc.kill()
    time.sleep(60)  # 休眠 60 秒后再次检查进程
