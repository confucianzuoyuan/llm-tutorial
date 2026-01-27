import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("mnist_train.csv")

print(data.head())

first_row = data.iloc[0]
label = first_row.iloc[0]
pixels = first_row.iloc[1:].values

# 将一维数组重塑为28x28的图像
image = pixels.reshape(28, 28)

# 创建图形
plt.figure(figsize=(6, 6))
plt.imshow(image, cmap='gray')
plt.title(f'Label: {int(label)}', fontsize=16)
plt.axis('off')
plt.colorbar(label='Pixel Intensity')
plt.tight_layout()
plt.show()

data = np.array(data)
print(data.shape)

m, n = data.shape

np.random.shuffle(data)

data_dev = data[0: 1000].T
Y_dev = data_dev[0]
X_dev = data_dev[1: n]
X_dev = X_dev / 255.0


data_train = data[1000: m].T
Y_train = data_train[0]
X_train = data_train[1: n]
X_train = X_train / 255.0
_, m_train = X_train.shape


def init_params():
    w1 = np.random.rand(10, 784) - 0.5
    b1 = np.random.rand(10, 1) - 0.5
    w2 = np.random.rand(10, 10) - 0.5
    b2 = np.random.rand(10, 1) - 0.5
    return w1, b1, w2, b2


def ReLU(Z):
    return np.maximum(Z, 0)


def softmax(Z):
    A = np.exp(Z) / sum(np.exp(Z))
    return A


def forward_prop(w1, b1, w2, b2, X):
    z1 = w1.dot(X)+b1
    a1 = ReLU(z1)
    z2 = w2.dot(a1)+b2
    a2 = softmax(z2)
    return z1, a1, z2, a2


def one_hot(Y):
    one_hot_Y = np.zeros((Y.size, Y.max() + 1))
    one_hot_Y[np.arange(Y.size), Y] = 1
    one_hot_Y = one_hot_Y.T
    return one_hot_Y


def deriv_ReLU(Z):
    return Z > 0

# z1, a1, z2, a2: M, A, Z, output
def back_prop(z1, a1, z2, a2, w2, Y, X):
    OneHot_Y = one_hot(Y)
    dZ2 = a2-OneHot_Y
    dW2 = 1/m * dZ2.dot(a1.T)
    db2 = 1/m * np.sum(dZ2, axis=1, keepdims=True)
    dZ1 = w2.T.dot(dZ2)*deriv_ReLU(z1)
    dW1 = 1/m * dZ1.dot(X.T)
    db1 = 1/m * np.sum(dZ1, axis=1, keepdims=True)
    return dW1, db1, dW2, db2


def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
    W1 = W1-alpha*dW1
    b1 = b1-alpha*db1
    W2 = W2-alpha*dW2
    b2 = b2-alpha*db2
    return W1, b1, W2, b2


def get_predictions(a2):
    return np.argmax(a2, 0)


def get_accuracy(predictions, Y):
    print(predictions, Y)
    return np.sum(predictions == Y)/Y.size


def gradient_descent(X, Y, iterations, alpha):
    w1, b1, w2, b2 = init_params()
    for i in range(iterations):
        z1, a1, z2, a2 = forward_prop(w1, b1, w2, b2, X)
        dW1, db1, dW2, db2 = back_prop(z1, a1, z2, a2, w2, Y, X)
        w1, b1, w2, b2 = update_params(
            w1, b1, w2, b2, dW1, db1, dW2, db2, alpha)
        if i % 10 == 0:
            print("iterations: ", i)
            print("accuracy: ", get_accuracy(get_predictions(a2), Y))
    return w1, b1, w2, b2


w1, b1, w2, b2 = gradient_descent(X_train, Y_train, 500, 0.1)


def make_predictions(X, W1, b1, W2, b2):
    _, _, _, A2 = forward_prop(W1, b1, W2, b2, X)
    predictions = get_predictions(A2)
    return predictions


def test_prediction(index, W1, b1, W2, b2):
    current_image = X_train[:, index, None]
    prediction = make_predictions(X_train[:, index, None], W1, b1, W2, b2)
    label = Y_train[index]
    print("Prediction: ", prediction)
    print("Label: ", label)

    current_image = current_image.reshape((28, 28)) * 255
    plt.gray()
    plt.imshow(current_image, interpolation='nearest')
    plt.show()


print(test_prediction(0, w1, b1, w2, b2))
print(test_prediction(1, w1, b1, w2, b2))
print(test_prediction(2, w1, b1, w2, b2))
print(test_prediction(3, w1, b1, w2, b2))

dev_predictions = make_predictions(X_dev, w1, b1, w2, b2)
print(get_accuracy(dev_predictions, Y_dev))
