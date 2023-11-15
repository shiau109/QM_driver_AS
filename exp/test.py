import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import curve_fit

# 生成示例数据（可以替换成你的实际数据）
np.random.seed(42)
# data = np.random.normal(loc=5, scale=2, size=1000)  # 平均值为5，标准差为2的正态分布
data = [1,2,3,4,5,6,7,8,9,10]
tmp = 0
for i in data:
    tmp += i
tmp = tmp/len(data)
print(tmp)
bin_width = 0.5
start_value = 0.75
end_value = 22.25
custom_bins = [start_value + i * bin_width for i in range(int((end_value - start_value) / bin_width) + 1)]
# 定义高斯分布的模型函数
def gaussian(x, mu, sigma):
    return norm.pdf(x, mu, sigma)

# 获取直方图的值

hist_values, bin_edges = np.histogram(data, bins=custom_bins, density=True)
bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
print(bin_centers)
print(hist_values)
# 使用 curve_fit 函数拟合高斯分布模型
params, covariance = curve_fit(gaussian, bin_centers, hist_values)

# 提取拟合的参数
mu, sigma = params

# 绘制直方图和拟合的高斯分布曲线
plt.hist(data, bins=custom_bins, density=True, alpha=0.7, color='blue', label='Histogram')
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = gaussian(x, mu, sigma)
plt.plot(x, p, 'k', linewidth=2, label=f'Fit result: $\mu$={mu:.2f}, $\sigma$={sigma:.2f}')

# 显示图例和标题
plt.legend()
plt.title('Gaussian Distribution Fit')

# 显示图形
plt.show()

# 输出拟合得到的平均值和标准差
print(f'Mean: {mu:.2f}')
print(f'Standard Deviation: {sigma:.2f}')


import numpy as np

my_list = [4, 1, 3, 7, 2, 9]

# 使用 argsort 找到排序后的索引
sorted_indices = np.argsort(my_list)

# 取排序后的数组的第二个索引，即第二小值在原数组中的索引
second_min_index = sorted_indices[1]
second_min_value = my_list[second_min_index]

print(f"第二小值的索引: {second_min_index}")
print(f"第二小值的值: {second_min_value}")
print(my_list)