import math


class Value:
    """保存一个标量值,以及这个值的梯度(导数)"""

    def __init__(self, data, _parents=(), _op=""):
        self.data = data
        self.grad = 0
        # 内部变量,用于自动微分计算图的构建
        self._backward = lambda: None
        self._prev = set(_parents)
        self._op = _op  # 产生当前Value的算子,用于可视化/调试

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), "+")

        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward

        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward

        return out

    def __pow__(self, other):
        # 支持 Value 类型的指数
        other_value = other if isinstance(other, Value) else Value(other)
        out = Value(self.data ** other_value.data, (self, other_value), '**')

        def _backward():
            # d/dx(a^b) = b * a^(b-1) * da + a^b * ln(a) * db
            if self.data > 0:  # 避免 log(0) 或负数的 log
                self.grad += (other_value.data * self.data**(other_value.data - 1)) * out.grad
                other_value.grad += (self.data ** other_value.data * math.log(self.data)) * out.grad
            else:
                # 对于 a <= 0 的情况,只计算幂律部分
                self.grad += (other_value.data * self.data**(other_value.data - 1)) * out.grad
        out._backward = _backward

        return out

    def backward(self):
        # topological order all of the children in the graph
        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for parent in v._prev:
                    build_topo(parent)
                topo.append(v)
        build_topo(self)

        # go one variable at a time and apply the chain rule to get its gradient
        self.grad = 1
        for v in reversed(topo):
            v._backward()

    def __neg__(self):  # -self
        return self * -1

    def __radd__(self, other):  # other + self
        return self + other

    def __sub__(self, other):  # self - other
        return self + (-other)

    def __rsub__(self, other):  # other - self
        return other + (-self)

    def __rmul__(self, other):  # other * self
        return self * other

    def __truediv__(self, other):  # self / other
        return self * other**-1

    def __rtruediv__(self, other):  # other / self
        return other * self**-1

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"


def f(x):
    # 修复: 直接使用传入的 Value 对象,不要重新包装
    v0 = x
    v1 = v0 ** 2
    v2 = Value(math.e) ** v1
    v3 = v2 ** 2
    y = v3
    return y


x = Value(0.5)
y = f(x)
print(f"y = {y}")
y.backward()
print(f"x.grad = {x.grad}")

# 验证梯度计算
# f(x) = (e^(x^2))^2 = e^(2x^2)
# f'(x) = e^(2x^2) * 4x
expected_grad = math.exp(2 * 0.5**2) * 4 * 0.5
print(f"Expected gradient: {expected_grad}")
print(f"Difference: {abs(x.grad - expected_grad)}")
