from base import *
from two import a,b,c,func
# 对任务进行canopy聚类
T1 = 30
T2 = 15
canopy = []
points = list(zip(tasks['lon'], tasks['lat']))
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
    num = sum([int((lon, lat) in j) for j in canopy])
    num = 0
    for j in canopy:
        if (lon, lat) in j:
            num += 1
    new_tasks.loc[i, 'price'] = 69.5 - num * 0.5

    add = 0
    if num == 1:
        for j in canopy:
            if (lon, lat) in j:
              add = len(j)
    new_tasks.loc[i, 'price'] += add * 0.5

new_tasks.to_excel("./three/任务修正金额数据.xls")

vips_fix = OrderedDict({})
vips_fix['会员编号'] = vips['number']
vips_fix['修正金额'] = np.array(np.log(vips.loc[:, 'credit'])//2*0.5)
vips_fix = pd.DataFrame(vips_fix)
vips_fix.to_excel("./three/会员修正金额数据.xls")

f = open('./three/原任务打包.txt', 'w')
for i in canopy:
    if len(i) > 1:
        for x, y in i:
            f.write(tasks[tasks['lon'] == x][tasks['lat'] == y]['number'].values[0])
            f.write('  ')

        f.write('\n')
f.close()

# 计算期望
from two import a,b,c,func
for i in range(len(new_tasks['lon'])):
    lon = new_tasks['lon'][i]
    lat = new_tasks['lat'][i]
    for j in canopy:
        if (lon, lat) in j:
            new_tasks.loc[i, 'price'] = np.max([new_tasks[new_tasks['lon'] == x][new_tasks['lat'] == y]['price'].values[0] for x, y in j])
print('新任务实现期望：', sum(func(new_tasks['price'], a, b, c)))