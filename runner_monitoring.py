import time

import info
from info import gl

# 获取所有GitLab Runner
runners = gl.runners.list(all=True)

# 初始化状态字典
status_dict = {'online': [], 'paused': [], 'offline': [], 'not connected': [], 'stuck': []}

while True:
    # 清空状态字典
    for key in status_dict.keys():
        status_dict[key] = []

    # 遍历所有Runner
    for runner in runners:
        # 获取Runner的状态
        status = runner.status

        # 将Runner根据状态添加到对应的列表中
        if status in status_dict:
            status_dict[status].append(runner)
        else:
            status_dict['not connected'].append(runner)

    # 打印各个状态的Runner数量
    print('Online: {}, Paused: {}, Offline: {}, Not Connected: {}, Stuck: {}'.format(
        len(status_dict['online']),
        len(status_dict['paused']),
        len(status_dict['offline']),
        len(status_dict['not connected']),
        len(status_dict['stuck'])
    ))

    # 等待5秒钟
    time.sleep(5)
