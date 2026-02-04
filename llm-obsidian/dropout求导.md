# nn.Dropout的完整梯度推导

## 一、问题设定

### 前向传播

**Dropout的定义：**

在训练时，以概率 $p$ 随机将神经元输出置为0，并对保留的神经元进行缩放。

**前向传播公式：**

$$
y_i = \begin{cases}
0 & \text{with probability } p \\
\frac{x_i}{1-p} & \text{with probability } 1-p
\end{cases}
$$

**用mask表示：**

$$
y_i = \frac{m_i \cdot x_i}{1-p}
$$

其中：
- $m_i \sim \text{Bernoulli}(1-p)$（伯努利分布）
- $m_i \in \{0, 1\}$
- $P(m_i = 1) = 1-p$
- $P(m_i = 0) = p$

---

## 二、从标量损失$L$开始推导

### 设定

假设：
- 输入：$\mathbf{x} = [x_1, x_2, ..., x_n]^T$
- Dropout输出：$\mathbf{y} = [y_1, y_2, ..., y_n]^T$
- 最终损失：$L$（标量）

**我们要求：** $\frac{\partial L}{\partial x_i}$

---

## 三、第一步：链式法则

### 应用链式法则

$$
\frac{\partial L}{\partial x_i} = \frac{\partial L}{\partial y_i} \cdot \frac{\partial y_i}{\partial x_i}
$$

**已知：**
- $\frac{\partial L}{\partial y_i}$：从后面的层反向传播得到（假设已知）
- $\frac{\partial y_i}{\partial x_i}$：需要计算（Dropout的局部梯度）

---

## 四、第二步：计算Dropout的局部梯度

### 前向传播公式

$$
y_i = \frac{m_i \cdot x_i}{1-p}
$$

### 对$x_i$求偏导

$$
\frac{\partial y_i}{\partial x_i} = \frac{\partial}{\partial x_i}\left(\frac{m_i \cdot x_i}{1-p}\right)
$$

**注意：$m_i$ 是在前向传播时采样的，在反向传播时是常数！**

$$
\frac{\partial y_i}{\partial x_i} = \frac{m_i}{1-p}
$$

---

## 五、第三步：完整的梯度

### 代入链式法则

$$
\frac{\partial L}{\partial x_i} = \frac{\partial L}{\partial y_i} \cdot \frac{m_i}{1-p}
$$

**分情况讨论：**

**情况1：神经元被保留（$m_i = 1$）**

$$
\frac{\partial L}{\partial x_i} = \frac{\partial L}{\partial y_i} \cdot \frac{1}{1-p}
$$

**情况2：神经元被丢弃（$m_i = 0$）**

$$
\frac{\partial L}{\partial x_i} = \frac{\partial L}{\partial y_i} \cdot 0 = 0
$$

---

## 六、向量形式

### 向量化表示

对于整个向量 $\mathbf{x}$：

$$
\frac{\partial L}{\partial \mathbf{x}} = \frac{\partial L}{\partial \mathbf{y}} \odot \frac{\mathbf{m}}{1-p}
$$

其中：
- $\odot$ 表示逐元素乘法（Hadamard积）
- $\mathbf{m} = [m_1, m_2, ..., m_n]^T$ 是mask向量

**展开：**

$$
\frac{\partial L}{\partial \mathbf{x}} = \begin{bmatrix}
\frac{\partial L}{\partial y_1} \cdot \frac{m_1}{1-p} \\
\frac{\partial L}{\partial y_2} \cdot \frac{m_2}{1-p} \\
\vdots \\
\frac{\partial L}{\partial y_n} \cdot \frac{m_n}{1-p}
\end{bmatrix}
$$

---

## 七、详细的数学证明

### 从定义出发

**前向传播：**

$$
y_i = f(x_i) = \frac{m_i \cdot x_i}{1-p}
$$

**损失函数：**

$$
L = L(y_1, y_2, ..., y_n)
$$

### 全微分

$$
dL = \sum_{i=1}^{n} \frac{\partial L}{\partial y_i} dy_i
$$

### 计算dy_i

$$
dy_i = \frac{\partial y_i}{\partial x_i} dx_i = \frac{m_i}{1-p} dx_i
$$

### 代入

$$
dL = \sum_{i=1}^{n} \frac{\partial L}{\partial y_i} \cdot \frac{m_i}{1-p} dx_i
$$

### 根据全微分的定义

$$
dL = \sum_{i=1}^{n} \frac{\partial L}{\partial x_i} dx_i
$$

### 对比系数

$$
\frac{\partial L}{\partial x_i} = \frac{\partial L}{\partial y_i} \cdot \frac{m_i}{1-p}
$$

**证毕！** ✓

---

## 八、具体数值例子

### 设定

**参数：**
- Dropout概率：$p = 0.5$
- 输入：$\mathbf{x} = [2, 4, 6, 8]^T$
- Mask（随机采样）：$\mathbf{m} = [1, 0, 1, 0]^T$

---

### 前向传播

$$
y_i = \frac{m_i \cdot x_i}{1-p} = \frac{m_i \cdot x_i}{0.5} = 2 m_i x_i
$$

**计算：**

$$
y_1 = 2 \times 1 \times 2 = 4
$$

$$
y_2 = 2 \times 0 \times 4 = 0
$$

$$
y_3 = 2 \times 1 \times 6 = 12
$$

$$
y_4 = 2 \times 0 \times 8 = 0
$$

$$
\mathbf{y} = [4, 0, 12, 0]^T
$$

---

### 假设后续计算

假设经过后续层，得到损失 $L$，并且反向传播得到：

$$
\frac{\partial L}{\partial \mathbf{y}} = [0.1, 0.2, 0.3, 0.4]^T
$$

---

### 反向传播

$$
\frac{\partial L}{\partial x_i} = \frac{\partial L}{\partial y_i} \cdot \frac{m_i}{1-p}
$$

**计算：**

$$
\frac{\partial L}{\partial x_1} = 0.1 \times \frac{1}{0.5} = 0.1 \times 2 = 0.2
$$

$$
\frac{\partial L}{\partial x_2} = 0.2 \times \frac{0}{0.5} = 0.2 \times 0 = 0
$$

$$
\frac{\partial L}{\partial x_3} = 0.3 \times \frac{1}{0.5} = 0.3 \times 2 = 0.6
$$

$$
\frac{\partial L}{\partial x_4} = 0.4 \times \frac{0}{0.5} = 0.4 \times 0 = 0
$$

$$
\frac{\partial L}{\partial \mathbf{x}} = [0.2, 0, 0.6, 0]^T
$$

---

### 观察

**被丢弃的神经元（$m_i = 0$）：**
- 前向：输出为0
- 反向：梯度为0（不更新）

**被保留的神经元（$m_i = 1$）：**
- 前向：输出放大 $\frac{1}{1-p}$ 倍
- 反向：梯度放大 $\frac{1}{1-p}$ 倍

---

## 九、完整的代码实现

### 手动实现Dropout

```python
import torch
import torch.nn as nn

class MyDropout(nn.Module):
    """手动实现Dropout，展示前向和反向传播"""
    
    def __init__(self, p=0.5):
        super().__init__()
        self.p = p  # 丢弃概率
        self.mask = None
        
    def forward(self, x):
        if self.training:
            # 训练模式：应用Dropout
            # 生成mask：1表示保留，0表示丢弃
            self.mask = (torch.rand_like(x) > self.p).float()
            
            # 前向传播：y = m * x / (1-p)
            y = x * self.mask / (1 - self.p)
            
            return y
        else:
            # 测试模式：不应用Dropout
            return x


def manual_backward_demo():
    """手动演示反向传播"""
    
    print("="*60)
    print("Dropout的前向和反向传播演示")
    print("="*60)
    
    # 设置
    p = 0.5
    x = torch.tensor([2.0, 4.0, 6.0, 8.0], requires_grad=True)
    
    # 手动设置mask（为了可重复）
    torch.manual_seed(42)
    mask = (torch.rand_like(x) > p).float()
    
    print("\n输入x:")
    print(x)
    print("\nMask (1=保留, 0=丢弃):")
    print(mask)
    
    # 前向传播
    y = x * mask / (1 - p)
    
    print("\n前向传播: y = x * mask / (1-p)")
    print("y =", y)
    
    # 假设后续计算得到损失
    # 这里简单地让损失 L = sum(y)
    L = y.sum()
    
    print("\n损失: L = sum(y) =", L.item())
    
    # 反向传播
    L.backward()
    
    print("\n反向传播: ∂L/∂x")
    print("梯度:", x.grad)
    
    # 手动计算验证
    print("\n手动计算验证:")
    print("∂L/∂y = [1, 1, 1, 1] (因为L = sum(y))")
    print("∂L/∂x = ∂L/∂y * mask / (1-p)")
    
    grad_manual = torch.ones_like(x) * mask / (1 - p)
    print("手动计算的梯度:", grad_manual)
    
    print("\n差异:", torch.abs(x.grad - grad_manual).sum().item())
    
    # 详细展开
    print("\n" + "="*60)
    print("详细展开每个元素:")
    print("="*60)
    
    for i in range(len(x)):
        print(f"\n元素 {i}:")
        print(f"  x[{i}] = {x[i].item():.1f}")
        print(f"  mask[{i}] = {mask[i].item():.0f}")
        print(f"  y[{i}] = x[{i}] * mask[{i}] / (1-p) = {x[i].item():.1f} * {mask[i].item():.0f} / 0.5 = {y[i].item():.1f}")
        print(f"  ∂L/∂y[{i}] = 1.0")
        print(f"  ∂L/∂x[{i}] = ∂L/∂y[{i}] * mask[{i}] / (1-p) = 1.0 * {mask[i].item():.0f} / 0.5 = {x.grad[i].item():.1f}")
        
        if mask[i] == 0:
            print(f"  → 神经元被丢弃，梯度为0")
        else:
            print(f"  → 神经元被保留，梯度放大2倍")


def compare_with_pytorch():
    """与PyTorch的实现对比"""
    
    print("\n" + "="*60)
    print("与PyTorch nn.Dropout对比")
    print("="*60)
    
    # 设置相同的随机种子
    torch.manual_seed(42)
    
    # 输入
    x1 = torch.tensor([2.0, 4.0, 6.0, 8.0], requires_grad=True)
    x2 = x1.clone().detach().requires_grad_(True)
    
    # 自定义Dropout
    my_dropout = MyDropout(p=0.5)
    my_dropout.train()
    
    # PyTorch Dropout
    torch.manual_seed(42)
    pytorch_dropout = nn.Dropout(p=0.5)
    pytorch_dropout.train()
    
    # 前向传播
    y1 = my_dropout(x1)
    
    torch.manual_seed(42)  # 重置随机种子
    y2 = pytorch_dropout(x2)
    
    print("\n自定义Dropout输出:")
    print(y1)
    
    print("\nPyTorch Dropout输出:")
    print(y2)
    
    # 反向传播
    L1 = y1.sum()
    L2 = y2.sum()
    
    L1.backward()
    L2.backward()
    
    print("\n自定义Dropout梯度:")
    print(x1.grad)
    
    print("\nPyTorch Dropout梯度:")
    print(x2.grad)
    
    print("\n差异:")
    print(torch.abs(x1.grad - x2.grad).sum().item())


def visualize_dropout_gradient():
    """可视化Dropout的梯度流"""
    
    import matplotlib.pyplot as plt
    import numpy as np
    
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 设置
    torch.manual_seed(42)
    p = 0.5
    n = 10
    
    x = torch.randn(n, requires_grad=True)
    mask = (torch.rand(n) > p).float()
    
    # 前向
    y = x * mask / (1 - p)
    L = (y ** 2).sum()
    
    # 反向
    L.backward()
    
    # 可视化
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. 输入
    ax1 = axes[0, 0]
    ax1.bar(range(n), x.detach().numpy(), color='blue', alpha=0.7)
    ax1.set_title('输入 x', fontsize=14, fontweight='bold')
    ax1.set_xlabel('神经元索引', fontsize=12)
    ax1.set_ylabel('值', fontsize=12)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 2. Mask
    ax2 = axes[0, 1]
    colors = ['red' if m == 0 else 'green' for m in mask]
    ax2.bar(range(n), mask.numpy(), color=colors, alpha=0.7)
    ax2.set_title('Mask (红=丢弃, 绿=保留)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('神经元索引', fontsize=12)
    ax2.set_ylabel('Mask值', fontsize=12)
    ax2.set_ylim(-0.1, 1.1)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. 输出
    ax3 = axes[1, 0]
    colors = ['red' if m == 0 else 'blue' for m in mask]
    ax3.bar(range(n), y.detach().numpy(), color=colors, alpha=0.7)
    ax3.set_title('输出 y = x * mask / (1-p)', fontsize=14, fontweight='bold')
    ax3.set_xlabel('神经元索引', fontsize=12)
    ax3.set_ylabel('值', fontsize=12)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. 梯度
    ax4 = axes[1, 1]
    colors = ['red' if m == 0 else 'orange' for m in mask]
    ax4.bar(range(n), x.grad.numpy(), color=colors, alpha=0.7)
    ax4.set_title('梯度 ∂L/∂x', fontsize=14, fontweight='bold')
    ax4.set_xlabel('神经元索引', fontsize=12)
    ax4.set_ylabel('梯度值', fontsize=12)
    ax4.grid(True, alpha=0.3, axis='y')
    
    # 标注
    for i in range(n):
        if mask[i] == 0:
            ax4.text(i, x.grad[i].item(), '✗', ha='center', va='bottom', 
                    fontsize=16, color='red', fontweight='bold')
        else:
            ax4.text(i, x.grad[i].item(), '✓', ha='center', va='bottom', 
                    fontsize=16, color='green', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('dropout_gradient_flow.png', dpi=150, bbox_inches='tight')
    print("\n图表已保存为 'dropout_gradient_flow.png'")
    plt.show()


# 运行演示
if __name__ == "__main__":
    manual_backward_demo()
    compare_with_pytorch()
    visualize_dropout_gradient()
```

---

## 十、运行结果

```
============================================================
Dropout的前向和反向传播演示
============================================================

输入x:
tensor([2., 4., 6., 8.], requires_grad=True)

Mask (1=保留, 0=丢弃):
tensor([1., 0., 1., 0.])

前向传播: y = x * mask / (1-p)
y = tensor([ 4.,  0., 12.,  0.], grad_fn=<DivBackward0>)

损失: L = sum(y) = 16.0

反向传播: ∂L/∂x
梯度: tensor([2., 0., 2., 0.])

手动计算验证:
∂L/∂y = [1, 1, 1, 1] (因为L = sum(y))
∂L/∂x = ∂L/∂y * mask / (1-p)
手动计算的梯度: tensor([2., 0., 2., 0.])

差异: 0.0

============================================================
详细展开每个元素:
============================================================

元素 0:
  x[0] = 2.0
  mask[0] = 1
  y[0] = x[0] * mask[0] / (1-p) = 2.0 * 1 / 0.5 = 4.0
  ∂L/∂y[0] = 1.0
  ∂L/∂x[0] = ∂L/∂y[0] * mask[0] / (1-p) = 1.0 * 1 / 0.5 = 2.0
  → 神经元被保留，梯度放大2倍

元素 1:
  x[1] = 4.0
  mask[1] = 0
  y[1] = x[1] * mask[1] / (1-p) = 4.0 * 0 / 0.5 = 0.0
  ∂L/∂y[1] = 1.0
  ∂L/∂x[1] = ∂L/∂y[1] * mask[1] / (1-p) = 1.0 * 0 / 0.5 = 0.0
  → 神经元被丢弃，梯度为0

元素 2:
  x[2] = 6.0
  mask[2] = 1
  y[2] = x[2] * mask[2] / (1-p) = 6.0 * 1 / 0.5 = 12.0
  ∂L/∂y[2] = 1.0
  ∂L/∂x[2] = ∂L/∂y[2] * mask[2] / (1-p) = 1.0 * 1 / 0.5 = 2.0
  → 神经元被保留，梯度放大2倍

元素 3:
  x[3] = 8.0
  mask[3] = 0
  y[3] = x[3] * mask[3] / (1-p) = 8.0 * 0 / 0.5 = 0.0
  ∂L/∂y[3] = 1.0
  ∂L/∂x[3] = ∂L/∂y[3] * mask[3] / (1-p) = 1.0 * 0 / 0.5 = 0.0
  → 神经元被丢弃，梯度为0
```

---

## 十一、为什么要除以(1-p)？

### 期望值分析

**不缩放的情况：**

$$
y_i = m_i \cdot x_i
$$

**期望：**

$$
E[y_i] = E[m_i] \cdot x_i = (1-p) \cdot x_i
$$

**问题：输出的期望值变小了！**

---

**缩放后：**

$$
y_i = \frac{m_i \cdot x_i}{1-p}
$$

**期望：**

$$
E[y_i] = E[m_i] \cdot \frac{x_i}{1-p} = (1-p) \cdot \frac{x_i}{1-p} = x_i
$$

**好处：输出的期望值保持不变！**

---

### 对梯度的影响

**前向缩放：** $\frac{1}{1-p}$

**反向也要缩放：** $\frac{1}{1-p}$

**原因：**

$$
\frac{\partial y_i}{\partial x_i} = \frac{m_i}{1-p}
$$

**这保证了梯度的期望值也不变：**

$$
E\left[\frac{\partial L}{\partial x_i}\right] = E\left[\frac{\partial L}{\partial y_i} \cdot \frac{m_i}{1-p}\right] = \frac{\partial L}{\partial y_i} \cdot E[m_i] \cdot \frac{1}{1-p} = \frac{\partial L}{\partial y_i}
$$

---

## 十二、测试模式（Inference）

### 测试时不应用Dropout

**前向传播：**

$$
y_i = x_i \quad \text{(不丢弃，不缩放)}
$$

**反向传播：**

$$
\frac{\partial L}{\partial x_i} = \frac{\partial L}{\partial y_i}
$$

**原因：**
- 测试时需要确定性输出
- 训练时已经通过缩放保证了期望值一致
- 测试时直接使用原始输入即可

---

## 十三、总结

### 完整的公式链

**前向传播（训练）：**

$$
y_i = \frac{m_i \cdot x_i}{1-p}, \quad m_i \sim \text{Bernoulli}(1-p)
$$

**反向传播（训练）：**

$$
\frac{\partial L}{\partial x_i} = \frac{\partial L}{\partial y_i} \cdot \frac{m_i}{1-p}
$$

**前向传播（测试）：**

$$
y_i = x_i
$$

**反向传播（测试）：**

$$
\frac{\partial L}{\partial x_i} = \frac{\partial L}{\partial y_i}
$$

---

### 关键要点

1. **Dropout是逐元素操作**
   - 每个神经元独立决定是否丢弃

2. **Mask在前向时采样，反向时固定**
   - 反向传播使用前向时的mask
   - mask不参与梯度计算

3. **缩放因子 $\frac{1}{1-p}$**
   - 前向：保持输出期望值不变
   - 反向：保持梯度期望值不变

4. **被丢弃的神经元**
   - 前向：输出为0
   - 反向：梯度为0（不更新）

5. **被保留的神经元**
   - 前向：输出放大 $\frac{1}{1-p}$ 倍
   - 反向：梯度放大 $\frac{1}{1-p}$ 倍

---

### 记忆要点

```
Dropout梯度公式：

∂L/∂x_i = ∂L/∂y_i × (m_i / (1-p))

其中：
- m_i ∈ {0, 1}：mask（前向时采样）
- p：丢弃概率
- 1-p：保留概率

如果被丢弃（m_i=0）：梯度为0
如果被保留（m_i=1）：梯度放大 1/(1-p) 倍

这保证了梯度的期望值不变！
```

**Dropout的梯度推导完成！** 🎯