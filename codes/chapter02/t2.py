import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['FZShuSong-Z01', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 创建图形和子图
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 第一个函数: f(x) = x/|x|
# 分段绘制,避免在x=0处连接
x1_neg = np.linspace(-2, -0.001, 150)
x1_pos = np.linspace(0.001, 2, 150)
y1_neg = x1_neg / np.abs(x1_neg)  # x < 0 时为 -1
y1_pos = x1_pos / np.abs(x1_pos)  # x > 0 时为 1

axes[0].plot(x1_neg, y1_neg, 'b-', linewidth=2, label=r'$f(x) = \frac{x}{|x|}$')
axes[0].plot(x1_pos, y1_pos, 'b-', linewidth=2)
# 在不连续点 (0, -1) 处画空心圆圈
axes[0].plot(0, -1, 'ro', markersize=8, markerfacecolor='white', 
             markeredgewidth=2, label='不连续点 (0, -1)')
# 在 (0, 1) 处也画一个空心圆圈表示右侧极限
axes[0].plot(0, 1, 'go', markersize=8, markerfacecolor='white', 
             markeredgewidth=2, label='右极限点 (0, 1)')
axes[0].set_xlabel('x', fontsize=12)
axes[0].set_ylabel('y', fontsize=12)
axes[0].set_title(r'函数: $f(x) = \frac{x}{|x|}$', fontsize=14, fontweight='bold')
axes[0].set_ylim(-2, 2)
axes[0].grid(True, alpha=0.3)
axes[0].legend(fontsize=10)
axes[0].axhline(y=0, color='k', linewidth=0.5)
axes[0].axvline(x=0, color='k', linewidth=0.5)

# 第二个函数: f(x) = √|x|
x2 = np.linspace(-2, 2, 400)
y2 = np.sqrt(np.abs(x2))

axes[1].plot(x2, y2, 'b-', linewidth=2, label=r'$f(x) = \sqrt{|x|}$')
axes[1].set_xlabel('x', fontsize=12)
axes[1].set_ylabel('y', fontsize=12)
axes[1].set_title(r'函数: $f(x) = \sqrt{|x|}$', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3)
axes[1].legend(fontsize=11)
axes[1].axhline(y=0, color='k', linewidth=0.5)
axes[1].axvline(x=0, color='k', linewidth=0.5)

# 第三个函数: f(x) = 1/x
# 分段绘制,避免在x=0处的渐近线连接
x3_neg = np.linspace(-2, -0.05, 200)
x3_pos = np.linspace(0.05, 2, 200)
y3_neg = 1 / x3_neg
y3_pos = 1 / x3_pos

axes[2].plot(x3_neg, y3_neg, 'b-', linewidth=2, label=r'$f(x) = \frac{1}{x}$')
axes[2].plot(x3_pos, y3_pos, 'b-', linewidth=2)
# 绘制渐近线
axes[2].axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.7, label='渐近线 x=0')
axes[2].set_xlabel('x', fontsize=12)
axes[2].set_ylabel('y', fontsize=12)
axes[2].set_title(r'函数: $f(x) = \frac{1}{x}$', fontsize=14, fontweight='bold')
axes[2].set_ylim(-10, 10)
axes[2].grid(True, alpha=0.3)
axes[2].legend(fontsize=11)
axes[2].axhline(y=0, color='k', linewidth=0.5)

# 调整子图间距
plt.tight_layout()

# 显示图形
plt.show()
