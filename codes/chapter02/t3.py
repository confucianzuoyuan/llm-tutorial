import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 创建图形和子图
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 定义x范围
x = np.linspace(-1.5, 1.5, 300)

# ========== 左图: 凸函数 (Convex) ==========
# 凸函数: f(x) = x^2
y_convex = x**2

# 绘制凸函数曲线
axes[0].plot(x, y_convex, 'b-', linewidth=2.5)

# 选择两个点绘制割线
x1, x2 = -1.2, 1.4
y1, y2 = x1**2, x2**2
axes[0].plot([x1, x2], [y1, y2], 'g-', linewidth=2)

# 标记两个端点
axes[0].plot(x1, y1, 'ko', markersize=8)
axes[0].plot(x2, y2, 'ko', markersize=8)

# 在中间点标记
x_mid = (x1 + x2) / 2
y_mid_line = (y1 + y2) / 2  # 割线上的点
y_mid_curve = x_mid**2  # 曲线上的点
axes[0].plot(x_mid, y_mid_line, 'ko', markersize=8)
axes[0].plot(x_mid, y_mid_curve, 'ko', markersize=8)

# 绘制垂直虚线连接
axes[0].plot([x_mid, x_mid], [y_mid_curve, y_mid_line], 'k--', linewidth=1.5, alpha=0.6)

# 设置标题和标签
axes[0].set_title('Convex', fontsize=16, fontweight='bold')
axes[0].set_xlim(-1.5, 1.5)
axes[0].set_ylim(0, 2.3)
axes[0].grid(True, alpha=0.4)
axes[0].set_xlabel('', fontsize=12)
axes[0].set_ylabel('', fontsize=12)

# ========== 右图: 非凸函数 (Non-convex) ==========
# 非凸函数: f(x) = x^3 - 3x
y_nonconvex = x**3 - 3*x

# 绘制非凸函数曲线
axes[1].plot(x, y_nonconvex, 'b-', linewidth=2.5)

# 选择两个点绘制割线
x1_nc, x2_nc = -1.2, 1.4
y1_nc = x1_nc**3 - 3*x1_nc
y2_nc = x2_nc**3 - 3*x2_nc
axes[1].plot([x1_nc, x2_nc], [y1_nc, y2_nc], 'g-', linewidth=2)

# 标记两个端点
axes[1].plot(x1_nc, y1_nc, 'ko', markersize=8)
axes[1].plot(x2_nc, y2_nc, 'ko', markersize=8)

# 设置标题和标签
axes[1].set_title('Non-convex', fontsize=16, fontweight='bold')
axes[1].set_xlim(-1.5, 1.5)
axes[1].set_ylim(-4.5, 4.5)
axes[1].grid(True, alpha=0.4)
axes[1].set_xlabel('', fontsize=12)
axes[1].set_ylabel('', fontsize=12)

# 调整布局
plt.tight_layout()

# 显示图形
plt.show()
