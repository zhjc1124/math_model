from base import *
import pandas as pd
from collections import OrderedDict

# 读取已结束任务信息
tasks_ = pd.read_excel('附件三：新项目任务数据.xls')
tasks = OrderedDict({})
tasks['number'] = tasks_['任务号码']
tasks['lon'] = tasks_["任务GPS经度"]
tasks['lat'] = tasks_["任务GPS纬度"]
tasks['price'] = np.zeros(len(tasks_))
tasks = pd.DataFrame(tasks)
# 对任务进行canopy聚类
T1 = 30
T2 = 15
canopy = []
points = list(zip(tasks['lon'], tasks['lat']))
from two import a,b,c,func
print('新任务实现期望：', sum(func(tasks['price'], a, b, c)))
while points:
    lon, lat = points[0]
    canopy.append([])
    d = get_distance(tasks['lon'], lon, tasks['lat'], lat)
    canopy[-1].extend(list(zip(tasks[d < T1]['lon'], tasks[d < T1]['lat'])))
    for x, y in zip(tasks[d < T2]['lon'], tasks[d < T2]['lat']):
        try:
            points.remove((x, y))
        except ValueError:
            pass

points = list(zip(tasks['lon'], tasks['lat']))

new_tasks = tasks.copy()
for i in range(len(new_tasks['lon'])):
    lon = new_tasks['lon'][i]
    lat = new_tasks['lat'][i]
    num = sum([int((lon, lat) in i) for i in canopy])
    new_tasks.loc[i, 'price'] = 69.5 - num * 0.5

    add = 0
    if num == 1:
        for j in canopy:
            if (lon, lat) in j:
              add = len(j)
    new_tasks.loc[i, 'price'] += add * 0.5

new_tasks.to_excel("./four/新任务定价.xls")

f = open('./four/新任务打包.txt', 'w')
for i in canopy:
    if len(i) > 1:
        for x, y in i:
            f.write(tasks[tasks['lon'] == x][tasks['lat'] == y]['number'].values[0])
            f.write('  ')

        f.write('\n')
f.close()


for i in range(len(new_tasks['lon'])):
    lon = new_tasks['lon'][i]
    lat = new_tasks['lat'][i]
    for j in canopy:
        if (lon, lat) in j:
            new_tasks.loc[i, 'price'] = np.max([new_tasks[new_tasks['lon'] == x][new_tasks['lat'] == y]['price'].values[0] for x, y in j])
print('新任务实现期望：', sum(func(new_tasks['price'], a, b, c)))
