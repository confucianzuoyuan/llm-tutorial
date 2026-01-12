import numpy as np
import matplotlib.pyplot as plt

# 创建图形和子图
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 第一个函数: f(x) = x²
x1 = np.linspace(-3, 3, 300)
y1 = x1**2
y1_derivative = 2*x1

axes[0].plot(x1, y1, 'b-', linewidth=2, label=r'$f(x) = x^2$')
axes[0].plot(x1, y1_derivative, 'r--', linewidth=1.5, label=r"$f'(x) = 2x$")
axes[0].set_xlabel('x', fontsize=12)
axes[0].set_ylabel('y', fontsize=12)
axes[0].set_title(r'$f(x) = x^2$', fontsize=14, fontweight='bold')
axes[0].grid(True, alpha=0.3)
axes[0].legend(fontsize=11)
axes[0].axhline(y=0, color='k', linewidth=0.5)
axes[0].axvline(x=0, color='k', linewidth=0.5)

# 第二个函数: f(x) = 3sin(x)
x2 = np.linspace(-3, 3, 300)
y2 = 3*np.sin(x2)
y2_derivative = 3*np.cos(x2)

axes[1].plot(x2, y2, 'b-', linewidth=2, label=r'$f(x) = 3\sin(x)$')
axes[1].plot(x2, y2_derivative, 'r--', linewidth=1.5,
             label=r"$f'(x) = 3\cos(x)$")
axes[1].set_xlabel('x', fontsize=12)
axes[1].set_ylabel('y', fontsize=12)
axes[1].set_title(r'$f(x) = 3\sin(x)$', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3)
axes[1].legend(fontsize=11)
axes[1].axhline(y=0, color='k', linewidth=0.5)
axes[1].axvline(x=0, color='k', linewidth=0.5)

# 第三个函数: f(x) = x³ - 5x
x3 = np.linspace(-2, 2, 300)
y3 = x3**3 - 5*x3
y3_derivative = 3*x3**2 - 5

axes[2].plot(x3, y3, 'b-', linewidth=2, label=r'$f(x) = x^3 - 5x$')
axes[2].plot(x3, y3_derivative, 'r--', linewidth=1.5,
             label=r"$f'(x) = 3x^2 - 5$")
axes[2].set_xlabel('x', fontsize=12)
axes[2].set_ylabel('y', fontsize=12)
axes[2].set_title(r'$f(x) = x^3 - 5x$', fontsize=14, fontweight='bold')
axes[2].grid(True, alpha=0.3)
axes[2].legend(fontsize=11)
axes[2].axhline(y=0, color='k', linewidth=0.5)
axes[2].axvline(x=0, color='k', linewidth=0.5)

# 调整子图间距
plt.tight_layout()

# 显示图形
plt.show()
