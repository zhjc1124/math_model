from base import *
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def func(x, a, b, c):
    y = a * (x + b)**2 + c
    return y


def polyfit(x, y):
    popt, pcov = curve_fit(func, x, y)
    return popt


# 每个价格区间的任务完成概率
prob_T.to_excel('./two/各价格区间的概率.xls')
dist_T.to_excel('./two/各价格区间的任务数.xls')
plt.figure(figsize=(10, 7))
ax = plt.gca()
plt.plot(prob_T['left'], prob_T['finished'])
ax.set_xlabel('价格区间')
ax.set_ylabel('任务完成概率')
plt.title('各价格区间的概率分布图')

# 删除部分不合理的值
prob_T_ = pd.read_excel('fixed各价格区间的概率.xls')
# 进行二次曲线拟合
a, b, c = polyfit(prob_T_['left'], prob_T_['finished'])
print('拟合曲线：y=%f*(x%f)**2+%f' % (a, b, c))
prob_T_updated = prob_T.copy()
prob_T_updated['finished'] = func(prob_T['left'], a, b, c)
prob_T_updated.to_excel("./two/各价格区间拟合后概率分布.xls")
plt.plot(prob_T_updated['left'], prob_T_updated['finished'])
plt.savefig('./two/各价格区间的概率分布图.png')
plt.show()

dist_sum = dist_T['finished'] + dist_T['unfinished']
price_mean = (dist_T['left']*dist_sum).sum()/dist_sum.sum()

print('原平均价格：', price_mean)
print('任务总数：', dist_sum.sum())
print('总价钱：', (dist_T['left']*dist_sum).sum())

l = 69.0
r = 69.5
l_num = 650
r_num = 185
print('原任务实现期望：', dist_T['finished'].sum())
print('新任务实现期望：', func(l, a, b, c)*l_num + func(r, a, b, c)*r_num)

