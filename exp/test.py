import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class CloseTo180Normalize(mcolors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=180, scale=10, clip=False):
        self.midpoint = midpoint
        self.scale = scale
        super().__init__(vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # 计算相对于midpoint的距离，并应用缩放因子
        x, y = [self.vmin, self.midpoint, self.midpoint, self.vmax], [0, 0.49, 0.51, 1]
        return np.ma.masked_array(np.interp(value, x, y))

# 生成示例数据
data = np.random.uniform(175, 185, (10, 10))  # 更集中于180附近的数据
data = np.array([[0,0,0],[1,1,1],[176,178,180]])

# 创建自定义归一化实例
norm = CloseTo180Normalize(vmin=175, vmax=185, midpoint=180, scale=10)

# 绘制数据
fig, ax = plt.subplots()
cax = ax.pcolor(data, cmap='coolwarm', norm=norm)

# 添加颜色条
fig.colorbar(cax, ax=ax)

plt.show()

test = [[[] for j in range(3)] for i in range(5) ]
print(test)