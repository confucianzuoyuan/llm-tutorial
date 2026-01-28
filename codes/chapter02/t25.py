import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
x = np.linspace(0, 1, 10)
y = np.sin(2 * np.pi * x) + 0.2 * np.random.randn(10)

# 拟合三次多项式：f(x) = w0 + w1*x + w2*x^2 + w3*x^3
# polyfit 返回系数从高次到低次：[w3, w2, w1, w0]
coeffs = np.polyfit(x, y, 3)
w3, w2, w1, w0 = coeffs

print(f"拟合结果:")
print(f"w0 = {w0:.4f}")
print(f"w1 = {w1:.4f}")
print(f"w2 = {w2:.4f}")
print(f"w3 = {w3:.4f}")

# 生成拟合曲线
x_fit = np.linspace(0, 1, 100)
y_fit = w0 + w1 * x_fit + w2 * (x_fit ** 2) + w3 * (x_fit ** 3)

# 绘图
plt.figure(figsize=(10, 6))
plt.scatter(x, y, s=100, c='blue', alpha=0.6, edgecolors='black', label='数据点')
plt.plot(x_fit, y_fit, 'r-', linewidth=2, label='三次多项式拟合')
plt.xlabel("x", fontsize=12)
plt.ylabel("y", fontsize=12)
plt.title("三次多项式拟合", fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
