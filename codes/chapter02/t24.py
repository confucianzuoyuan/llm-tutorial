import numpy as np
import matplotlib.pyplot as plt


np.random.seed(0)
x = np.linspace(0, 1, 10)
y = np.sin(2 * np.pi * x) + 0.2 * np.random.randn(10)

real_x = np.linspace(0, 1, 1000)
real_y = np.sin(2 * np.pi * real_x)

plt.scatter(x, y, s=100)
plt.plot(real_x, real_y, "g")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
