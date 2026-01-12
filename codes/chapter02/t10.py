import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
x = np.random.rand(100, 1)
y = 5 + 2 * x + np.random.rand(100, 1)

# Plot
plt.scatter(x, y, s=10)
plt.xlabel('x')
plt.ylabel('y')
plt.show()

W = 0
b = 0


def predict(x):
    """根据输入x做出预测"""
    y = W * x + b
    return y


def mean_squared_error(x0, x1):
    diff = x0 - x1
    return np.sum(diff ** 2) / len(diff)


def gradient(x, y, W, b):
    N = len(x)
    W_grad = 2 / N * sum((W * x_i[0] + b - y_i[0]) * x_i[0] for (x_i, y_i) in zip(x, y))
    b_grad = 2 / N * sum((W * x_i[0] + b - y_i[0]) for (x_i, y_i) in zip(x, y))
    return W_grad, b_grad

print(gradient(x, y, W, b))

lr = 0.1
iters = 100

for i in range(iters):
    y_pred = predict(x)
    loss = mean_squared_error(y, y_pred)

    W_grad, b_grad = gradient(x, y, W, b)
    W = W - lr * W_grad
    b = b - lr * b_grad
    print(W, b, loss)
    
# Plot
plt.scatter(x, y, s=10)
plt.xlabel('x')
plt.ylabel('y')
y_pred = predict(x)
plt.plot(x, y_pred, color='r')
plt.show()