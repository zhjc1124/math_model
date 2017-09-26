from base import *


# 每个区域任务数量热力图
plt.figure(figsize=(10, 7))
ax = plt.gca()
seaborn.heatmap(hm_tasks, cmap="YlGnBu")
ax.set_xlabel('经度（°）')
ax.set_ylabel('纬度（°）')
ax.set_xticklabels([str(ll_lon)]+[''] * (columns - 2)+[str(ur_lon)])
ax.set_yticklabels([str(ur_lat)]+[''] * (rows - 2)+[str(ll_lat)])
plt.title('区域任务数量热力图')
plt.savefig('./one/区域的任务数量.png')
plt.show()

price_mean = price_sum/hm_tasks

# 每个区域的平均价格热力图
plt.figure(figsize=(10, 7))
ax = plt.gca()
seaborn.heatmap(price_mean, cmap="YlGnBu")
ax.set_xlabel('经度（°）')
ax.set_ylabel('纬度（°）')
ax.set_xticklabels([str(ll_lon)]+[''] * (columns - 2)+[str(ur_lon)])
ax.set_yticklabels([str(ur_lat)]+[''] * (rows - 2)+[str(ll_lat)])
plt.title('区域平均价格热力图')
plt.savefig('./one/区域平均价格.png')
plt.show()


# 每个区域的会员分布热力图
plt.figure(figsize=(10, 7))
ax = plt.gca()
seaborn.heatmap(hm_vips, cmap="YlGnBu")
ax.set_xlabel('经度（°）')
ax.set_ylabel('纬度（°）')
ax.set_xticklabels([str(ll_lon)]+[''] * (columns - 2)+[str(ur_lon)])
ax.set_yticklabels([str(ur_lat)]+[''] * (rows - 2)+[str(ll_lat)])
plt.title('区域会员分布热力图')
plt.savefig('./one/区域会员分布.png')
plt.show()

# 每个区域会员-价格散点图
plt.figure(figsize=(10, 7))
ax = plt.gca()
plt.scatter(hm_vips.flatten(), price_mean.flatten(), marker='o', c='g')
ax.set_xlabel('区域会员数（个）')
ax.set_ylabel('区域价格平均值（元）')
plt.title('区域会员-价格散点图')
plt.savefig('./one/区域会员-价格散点图.png')
plt.show()


# 每个任务会员最近距离-价格散点图
plt.figure(figsize=(10, 7))
ax = plt.gca()
plt.scatter(min_d, tasks['price'], marker='o', c='g')
ax.set_xlabel('任务最近会员距离（km）')
ax.set_ylabel('任务价格（元）')
plt.title('任务最近会员距离-价格散点图')
plt.savefig('./one/任务-最近会员散点图.png')
plt.show()


# 已完成任务会员最近距离直方图
plt.figure(figsize=(10, 7))
ax = plt.gca()
plt.hist(min_d[tasks['finished'] == 1], bins=90)
ax.set_xlabel('已完成任务最近会员距离（km）')
ax.set_ylabel('已完成任务数目')
plt.title('已完成任务会员最近距离直方图')
plt.savefig('./one/已完成任务会员最近距离直方图.png')
plt.show()


# 未完成任务会员最近距离直方图
plt.figure(figsize=(10, 7))
ax = plt.gca()
plt.hist(min_d[(tasks['finished'] == 0)], bins=90)
ax.set_xlabel('未完成任务最近会员距离（km）')
ax.set_ylabel('未完成任务数目')
plt.title('未完成任务会员最近距离直方图')
plt.savefig('./one/未完成任务会员最近距离直方图.png')
plt.show()


# 每个区域已完成任务与会员数的关系图
plt.figure(figsize=(10, 7))
ax = plt.gca()
plt.scatter(hm_vips.ravel(), hm_tasks_T.ravel(), c='g')
ax.set_xlabel('每个区域已完成任务')
ax.set_ylabel('每个区域会员数')
plt.title('已完成任务与会员数关系图')
plt.savefig('./one/已完成任务与会员数的关系图.png')
plt.show()


# 每个区域已完成任务与价格关系
plt.figure(figsize=(10, 7))
ax = plt.gca()
plt.scatter(hm_tasks_T.ravel(), price_mean.ravel(), c='g')
ax.set_xlabel('每个区域已完成任务')
ax.set_ylabel('每个区域平均价格')
plt.title('已完成任务与平均价格关系图')
plt.savefig('./one/已完成任务与价格的关系图.png')
plt.show()


# 每个区域未完成任务与会员数的关系图
plt.figure(figsize=(10, 7))
ax = plt.gca()
plt.scatter(hm_vips.ravel(), hm_tasks_F.ravel(), c='g')
ax.set_xlabel('每个区域未完成任务')
ax.set_ylabel('每个区域会员数')
plt.title('未完成任务与会员数关系图')
plt.savefig('./one/未完成任务与会员数的关系图.png')
plt.show()


# 每个区域未完成任务与价格关系
plt.figure(figsize=(10, 7))
ax = plt.gca()
plt.scatter( hm_tasks_F.ravel(), price_mean.ravel(), c='g')
ax.set_xlabel('每个区域未完成任务')
ax.set_ylabel('每个区域平均价格')
plt.title('未完成任务与平均价格关系图')
plt.savefig('./one/未完成任务与价格的关系图.png')
plt.show()

