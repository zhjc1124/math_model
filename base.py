import pandas as pd
import numpy as np
from collections import OrderedDict


# 读取已结束任务信息
tasks_ = pd.read_excel('附件一：已结束项目任务数据.xls')
tasks = OrderedDict({})
tasks['number'] = tasks_['任务号码']
tasks['lon'] = tasks_["任务gps经度"]
tasks['lat'] = tasks_["任务gps 纬度"]
tasks['price'] = tasks_["任务标价"]
tasks['finished'] = tasks_["任务执行情况"]
tasks = pd.DataFrame(tasks)


# 读取会员信息
vips_ = pd.read_excel('附件二：会员信息数据.xlsx')
vips = OrderedDict({})
vips['number'] = vips_['会员编号']
vips['limit'] = vips_['预订任务限额']
vips['time'] = vips_['预订任务开始时间']
vips['credit'] = vips_['信誉值']
vips['lon'] = [float(i.split()[1]) for i in np.array(vips_['会员位置(GPS)'])]
vips['lat'] = [float(i.split()[0]) for i in np.array(vips_['会员位置(GPS)'])]
vips = pd.DataFrame(vips)

# 有一条经纬度错了的数据
for i in range(len(vips)):
    if vips.loc[i, 'lat'] > 100:
        vips.loc[i, 'lon'], vips.loc[i, 'lat'] = vips.loc[i, 'lat'], vips.loc[i, 'lon']


# 经纬度转换距离
EARTH_RADIUS = 6371


def hav(theta):
    s = np.sin(theta / 2)
    return s * s


# 计算最短距离
def get_distance(a_lon, b_lon, a_lat, b_lat):
    dlon = np.fabs(a_lon-b_lon)
    dlat = np.fabs(a_lat-b_lat)
    h = hav(dlat) + np.cos(a_lat) * np.cos(b_lat) * hav(dlon)
    distance = 2 * EARTH_RADIUS * np.arcsin(np.sqrt(h))
    return distance


vips_lat = np.radians(vips['lat'])
vips_lon = np.radians(vips['lon'])
tasks_lat = np.radians(tasks['lat'])
tasks_lon = np.radians(tasks['lon'])
min_d = np.zeros(len(tasks['lat']))
for i in range(len(tasks['lat'])):
    dlon = np.fabs(vips_lon - tasks_lon[i])
    dlat = np.fabs(vips_lat - tasks_lat[i])
    h = hav(dlat) + np.cos(vips_lat) * np.cos(tasks_lat) * hav(dlon)
    distance = 2 * EARTH_RADIUS * np.arcsin(np.sqrt(h))
    min_d[i] = distance.min()


ll_lon, ur_lon = 112.8, 114.5
ll_lat, ur_lat = 22.4, 23.6


rows, columns = 30, 30
hm_tasks = np.zeros([rows, columns])
price_sum = np.zeros([rows, columns])
lon_span, lat_span = 1/columns*(ur_lon-ll_lon), 1/rows*(ur_lat-ll_lat)

for lat, lon, price in zip(tasks['lat'], tasks['lon'], tasks['price']):
    for row in range(rows):
        if lat + (row+1) * lat_span > ur_lat:
            for column in range(columns):
                if lon - (column+1)*lon_span < ll_lon:
                    hm_tasks[row][column] += 1
                    price_sum[row][column] += price
                    break
            break


hm_vips = np.zeros([rows, columns])

for lat, lon in zip(vips['lat'], vips['lon']):
    for row in range(rows):
        if lat + (row+1) * lat_span > ur_lat:
            for column in range(columns):
                if lon - (column+1)*lon_span < ll_lon:
                    hm_vips[row][column] += 1
                    break
            break


tasks_T = tasks[tasks['finished'] == 1]
hm_tasks_T = np.zeros([rows, columns])
for lat, lon in zip(tasks_T['lat'], tasks_T['lon']):
    for row in range(rows):
        if lat + (row+1) * lat_span > ur_lat:
            for column in range(columns):
                if lon - (column+1)*lon_span < ll_lon:
                    hm_tasks_T[row][column] += 1
                    break
            break


tasks_F = tasks[tasks['finished'] != 1]
hm_tasks_F = np.zeros([rows, columns])
for lat, lon in zip(tasks_F['lat'], tasks_F['lon']):
    for row in range(rows):
        if lat + (row+1) * lat_span > ur_lat:
            for column in range(columns):
                if lon - (column+1)*lon_span < ll_lon:
                    hm_tasks_F[row][column] += 1
                    break
            break

price_span = 0.5
price_array = np.arange(64, 91, price_span)

prob_T = OrderedDict()
prob_T['left'] = []
prob_T['finished'] = []
prob_T['unfinished'] = []
dist_T = OrderedDict()
dist_T['left'] = []
dist_T['finished'] = []
dist_T['unfinished'] = []
for i in range(len(price_array)-1):
    m = tasks[tasks['price'] >= price_array[i]]
    n = m[m['price'] < price_array[i+1]]
    if len(n[n['finished'] == 1]):
        prob_T['left'].append(price_array[i])
        prob_T['finished'].append(len(n[n['finished'] == 1])/len(n))
        prob_T['unfinished'].append(len(n[n['finished'] == 0])/len(n))
        dist_T['left'].append(price_array[i])
        dist_T['finished'].append(len(n[n['finished'] == 1]))
        dist_T['unfinished'].append(len(n[n['finished'] == 0]))

prob_T = pd.DataFrame(prob_T)
dist_T = pd.DataFrame(dist_T)