# torch.einsum 完全指南

## 一、什么是einsum？

### 基本概念

**einsum = Einstein Summation（爱因斯坦求和约定）**

这是一种用简洁符号表示张量运算的方法，由爱因斯坦在相对论中提出。

**核心思想：**
- 用字母表示张量的维度
- 重复的字母表示求和
- 不出现在输出的字母表示被求和掉

---

### 语法

```python
torch.einsum(equation, *operands)
```

**参数：**
- `equation`：字符串，描述运算规则
- `*operands`：输入张量

**格式：**
```
"输入1索引,输入2索引,...->输出索引"
```

---

## 二、基础规则

### 规则1：维度标记

```python
import torch

# 一个矩阵 [3, 4]
A = torch.randn(3, 4)

# 用 'ij' 表示：i是第0维(3), j是第1维(4)
# i 对应行，j 对应列
```

**字母的含义：**
- 每个字母代表一个维度
- 字母的顺序对应张量的维度顺序
- 通常用 i, j, k, l, m, n...

---

### 规则2：重复字母 = 求和

```python
# 'ii' 表示对角线元素求和（trace）
A = torch.tensor([[1, 2],
                  [3, 4]])

result = torch.einsum('ii', A)
# 等价于：A[0,0] + A[1,1] = 1 + 4 = 5
print(result)  # tensor(5)
```

---

### 规则3：箭头右边 = 输出维度

```python
# 'ij->ji' 表示转置
A = torch.randn(3, 4)
result = torch.einsum('ij->ji', A)
# result.shape = [4, 3]
```

---

### 规则4：省略箭头 = 自动推断

```python
# 省略 '->' 时，输出包含所有只出现一次的字母（按字母顺序）
A = torch.randn(3, 4)
result = torch.einsum('ij', A)
# 等价于 'ij->ij'，即返回原矩阵
```

---

## 三、常见操作示例

### 1. 转置（Transpose）

```python
A = torch.randn(3, 4)

# 方法1：einsum
result = torch.einsum('ij->ji', A)

# 方法2：传统
result = A.T

print(result.shape)  # [4, 3]
```

**解释：**
```
输入：'ij' 表示 A[i, j]
输出：'ji' 表示结果[j, i]
→ 行列互换
```

---

### 2. 求和（Sum）

#### 全部求和

```python
A = torch.tensor([[1, 2, 3],
                  [4, 5, 6]])

# einsum：不指定输出维度 = 全部求和
result = torch.einsum('ij->', A)
# 等价于：A.sum()

print(result)  # tensor(21) = 1+2+3+4+5+6
```

#### 按行求和

```python
# 'ij->i' 保留i维度，对j求和
result = torch.einsum('ij->i', A)
# 等价于：A.sum(dim=1)

print(result)  # tensor([6, 15])
# 6 = 1+2+3
# 15 = 4+5+6
```

#### 按列求和

```python
# 'ij->j' 保留j维度，对i求和
result = torch.einsum('ij->j', A)
# 等价于：A.sum(dim=0)

print(result)  # tensor([5, 7, 9])
# 5 = 1+4
# 7 = 2+5
# 9 = 3+6
```

---

### 3. 对角线（Diagonal）

```python
A = torch.tensor([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

# 提取对角线
result = torch.einsum('ii->i', A)
# 等价于：torch.diag(A)

print(result)  # tensor([1, 5, 9])
```

**注意：这里输入是'ii'（两个i），但输出是'i'（一个i）**

---

### 4. 迹（Trace）

```python
A = torch.tensor([[1, 2],
                  [3, 4]])

# 对角线元素求和
result = torch.einsum('ii->', A)
# 等价于：torch.trace(A)

print(result)  # tensor(5) = 1+4
```

---

### 5. 矩阵乘法（Matrix Multiplication）

```python
A = torch.randn(3, 4)  # [3, 4]
B = torch.randn(4, 5)  # [4, 5]

# einsum
result = torch.einsum('ik,kj->ij', A, B)
# 等价于：A @ B

print(result.shape)  # [3, 5]
```

**详细解释：**

$$
C_{ij} = \sum_{k} A_{ik} B_{kj}
$$

```
'ik,kj->ij'
 ↓   ↓   ↓
 A   B   C

- A的维度：i(3), k(4)
- B的维度：k(4), j(5)
- k重复 → 对k求和
- 输出：i(3), j(5)
```

---

### 6. 批量矩阵乘法（Batch Matrix Multiplication）

```python
A = torch.randn(10, 3, 4)  # [batch, 3, 4]
B = torch.randn(10, 4, 5)  # [batch, 4, 5]

# einsum
result = torch.einsum('bik,bkj->bij', A, B)
# 等价于：torch.bmm(A, B)

print(result.shape)  # [10, 3, 5]
```

**解释：**
```
'bik,bkj->bij'
 ↓    ↓    ↓
 A    B    C

- b：batch维度（不求和，保留）
- i, j：矩阵维度（保留）
- k：重复 → 求和
```

---

### 7. 向量点积（Dot Product）

```python
a = torch.tensor([1, 2, 3])
b = torch.tensor([4, 5, 6])

# einsum
result = torch.einsum('i,i->', a, b)
# 等价于：torch.dot(a, b)

print(result)  # tensor(32) = 1*4 + 2*5 + 3*6
```

**解释：**
```
'i,i->'
 ↓ ↓  ↓
 a b  标量

- i重复两次 → 对i求和
- 输出为标量（无维度）
```

---

### 8. 外积（Outer Product）

```python
a = torch.tensor([1, 2, 3])
b = torch.tensor([4, 5])

# einsum
result = torch.einsum('i,j->ij', a, b)
# 等价于：torch.outer(a, b)

print(result)
# tensor([[ 4,  5],
#         [ 8, 10],
#         [12, 15]])
```

**解释：**

$$
C_{ij} = a_i \times b_j
$$

```
'i,j->ij'
 ↓ ↓  ↓
 a b  矩阵

- i, j 都不重复 → 不求和
- 输出：i×j 的矩阵
```

---

### 9. 批量点积（Batch Dot Product）

```python
A = torch.randn(10, 3)  # [batch, dim]
B = torch.randn(10, 3)  # [batch, dim]

# 每个样本计算点积
result = torch.einsum('bi,bi->b', A, B)

print(result.shape)  # [10]
```

**解释：**
```
'bi,bi->b'
 ↓   ↓  ↓
 A   B  向量

- b：batch维度（保留）
- i：重复 → 对i求和
- 输出：长度为batch的向量
```

---

### 10. Hadamard积（逐元素乘法）

```python
A = torch.randn(3, 4)
B = torch.randn(3, 4)

# einsum
result = torch.einsum('ij,ij->ij', A, B)
# 等价于：A * B

print(result.shape)  # [3, 4]
```

---

## 四、高级应用

### 1. 注意力机制（Attention）

```python
# Q: [batch, seq_len, d_k]
# K: [batch, seq_len, d_k]
# V: [batch, seq_len, d_v]

Q = torch.randn(2, 10, 64)  # [batch, seq_q, d_k]
K = torch.randn(2, 20, 64)  # [batch, seq_k, d_k]
V = torch.randn(2, 20, 128) # [batch, seq_k, d_v]

# 计算注意力分数：Q @ K.T
scores = torch.einsum('bqd,bkd->bqk', Q, K)
# scores.shape = [2, 10, 20]

# 等价于：
# scores = torch.matmul(Q, K.transpose(-2, -1))

# 注意力加权
attention = torch.softmax(scores, dim=-1)
output = torch.einsum('bqk,bkv->bqv', attention, V)
# output.shape = [2, 10, 128]
```

**完整的Attention：**

```python
def attention_einsum(Q, K, V):
    """
    Q: [batch, seq_q, d_k]
    K: [batch, seq_k, d_k]
    V: [batch, seq_k, d_v]
    """
    d_k = Q.shape[-1]
    
    # 计算注意力分数
    scores = torch.einsum('bqd,bkd->bqk', Q, K) / (d_k ** 0.5)
    
    # Softmax
    attention = torch.softmax(scores, dim=-1)
    
    # 加权求和
    output = torch.einsum('bqk,bkv->bqv', attention, V)
    
    return output, attention

# 测试
Q = torch.randn(2, 10, 64)
K = torch.randn(2, 20, 64)
V = torch.randn(2, 20, 128)

output, attn = attention_einsum(Q, K, V)
print(output.shape)  # [2, 10, 128]
print(attn.shape)    # [2, 10, 20]
```

---

### 2. 多头注意力（Multi-Head Attention）

```python
# Q, K, V: [batch, num_heads, seq_len, d_k]
Q = torch.randn(2, 8, 10, 64)  # [batch, heads, seq, d_k]
K = torch.randn(2, 8, 20, 64)
V = torch.randn(2, 8, 20, 64)

# 计算所有头的注意力分数
scores = torch.einsum('bhqd,bhkd->bhqk', Q, K)
# scores.shape = [2, 8, 10, 20]

attention = torch.softmax(scores, dim=-1)
output = torch.einsum('bhqk,bhkv->bhqv', attention, V)
# output.shape = [2, 8, 10, 64]
```

---

### 3. 双线性层（Bilinear Layer）

```python
# 双线性变换：y = x1^T W x2

x1 = torch.randn(32, 10)  # [batch, dim1]
x2 = torch.randn(32, 20)  # [batch, dim2]
W = torch.randn(10, 20)   # [dim1, dim2]

# einsum实现
result = torch.einsum('bi,ij,bj->b', x1, W, x2)
# result.shape = [32]

# 等价于：
# result = (x1 @ W * x2).sum(dim=1)
```

---

### 4. 张量收缩（Tensor Contraction）

```python
# 四维张量的复杂运算
A = torch.randn(3, 4, 5, 6)
B = torch.randn(5, 6, 7, 8)

# 对维度2和3收缩
result = torch.einsum('ijkl,klmn->ijmn', A, B)
# result.shape = [3, 4, 7, 8]
```

**解释：**
```
A: [i=3, j=4, k=5, l=6]
B: [k=5, l=6, m=7, n=8]

k, l 重复 → 求和
输出：[i=3, j=4, m=7, n=8]
```

---

### 5. 批量外积

```python
# 对batch中的每个样本计算外积
A = torch.randn(10, 3)  # [batch, dim1]
B = torch.randn(10, 4)  # [batch, dim2]

result = torch.einsum('bi,bj->bij', A, B)
# result.shape = [10, 3, 4]

print(result[0])  # 第一个样本的外积
```

---

### 6. 协方差矩阵

```python
# X: [n_samples, n_features]
X = torch.randn(100, 10)

# 中心化
X_centered = X - X.mean(dim=0, keepdim=True)

# 协方差矩阵
cov = torch.einsum('ni,nj->ij', X_centered, X_centered) / (X.shape[0] - 1)
# cov.shape = [10, 10]

# 等价于：
# cov = (X_centered.T @ X_centered) / (X.shape[0] - 1)
```

---

## 五、完整的对比示例

```python
import torch
import time

def compare_operations():
    """对比einsum和传统方法"""
    
    print("="*60)
    print("einsum vs 传统方法对比")
    print("="*60)
    
    # 1. 矩阵乘法
    print("\n1. 矩阵乘法")
    A = torch.randn(1000, 500)
    B = torch.randn(500, 300)
    
    # einsum
    start = time.time()
    result1 = torch.einsum('ik,kj->ij', A, B)
    time1 = time.time() - start
    
    # 传统
    start = time.time()
    result2 = A @ B
    time2 = time.time() - start
    
    print(f"  einsum: {time1:.6f}s")
    print(f"  传统:   {time2:.6f}s")
    print(f"  差异:   {torch.abs(result1 - result2).max().item():.2e}")
    
    # 2. 批量矩阵乘法
    print("\n2. 批量矩阵乘法")
    A = torch.randn(32, 100, 50)
    B = torch.randn(32, 50, 30)
    
    # einsum
    start = time.time()
    result1 = torch.einsum('bik,bkj->bij', A, B)
    time1 = time.time() - start
    
    # 传统
    start = time.time()
    result2 = torch.bmm(A, B)
    time2 = time.time() - start
    
    print(f"  einsum: {time1:.6f}s")
    print(f"  传统:   {time2:.6f}s")
    print(f"  差异:   {torch.abs(result1 - result2).max().item():.2e}")
    
    # 3. 注意力计算
    print("\n3. 注意力计算")
    Q = torch.randn(32, 10, 64)
    K = torch.randn(32, 20, 64)
    V = torch.randn(32, 20, 128)
    
    # einsum
    start = time.time()
    scores1 = torch.einsum('bqd,bkd->bqk', Q, K)
    attn1 = torch.softmax(scores1, dim=-1)
    output1 = torch.einsum('bqk,bkv->bqv', attn1, V)
    time1 = time.time() - start
    
    # 传统
    start = time.time()
    scores2 = torch.matmul(Q, K.transpose(-2, -1))
    attn2 = torch.softmax(scores2, dim=-1)
    output2 = torch.matmul(attn2, V)
    time2 = time.time() - start
    
    print(f"  einsum: {time1:.6f}s")
    print(f"  传统:   {time2:.6f}s")
    print(f"  差异:   {torch.abs(output1 - output2).max().item():.2e}")
    
    # 4. 复杂张量运算
    print("\n4. 四维张量收缩")
    A = torch.randn(10, 20, 30, 40)
    B = torch.randn(30, 40, 50, 60)
    
    # einsum
    start = time.time()
    result1 = torch.einsum('ijkl,klmn->ijmn', A, B)
    time1 = time.time() - start
    
    # 传统（需要reshape和多次操作）
    start = time.time()
    A_reshaped = A.reshape(10*20, 30*40)
    B_reshaped = B.reshape(30*40, 50*60)
    result2_temp = A_reshaped @ B_reshaped
    result2 = result2_temp.reshape(10, 20, 50, 60)
    time2 = time.time() - start
    
    print(f"  einsum: {time1:.6f}s")
    print(f"  传统:   {time2:.6f}s")
    print(f"  差异:   {torch.abs(result1 - result2).max().item():.2e}")


def einsum_cheatsheet():
    """einsum速查表"""
    
    print("\n" + "="*60)
    print("einsum速查表")
    print("="*60)
    
    examples = [
        ("转置", "ij->ji", "A.T"),
        ("求和", "ij->", "A.sum()"),
        ("按行求和", "ij->i", "A.sum(dim=1)"),
        ("按列求和", "ij->j", "A.sum(dim=0)"),
        ("对角线", "ii->i", "torch.diag(A)"),
        ("迹", "ii->", "torch.trace(A)"),
        ("矩阵乘法", "ik,kj->ij", "A @ B"),
        ("批量矩阵乘法", "bik,bkj->bij", "torch.bmm(A, B)"),
        ("向量点积", "i,i->", "torch.dot(a, b)"),
        ("外积", "i,j->ij", "torch.outer(a, b)"),
        ("逐元素乘法", "ij,ij->ij", "A * B"),
        ("批量点积", "bi,bi->b", "(A * B).sum(dim=1)"),
    ]
    
    print(f"\n{'操作':<15} {'einsum':<20} {'等价方法':<20}")
    print("-"*60)
    for name, einsum_str, equiv in examples:
        print(f"{name:<15} {einsum_str:<20} {equiv:<20}")


# 运行
if __name__ == "__main__":
    compare_operations()
    einsum_cheatsheet()
```

---

## 六、einsum的优缺点

### 优点 ✅

**1. 简洁表达**
```python
# 复杂的张量运算一行搞定
result = torch.einsum('bqhd,bkhd->bhqk', Q, K)

# 传统方法需要多步
Q_reshaped = Q.permute(0, 2, 1, 3)
K_reshaped = K.permute(0, 2, 3, 1)
result = torch.matmul(Q_reshaped, K_reshaped)
```

**2. 可读性强**
```python
# 'bik,bkj->bij' 清楚地表达了维度关系
# 一眼就能看出哪些维度求和，哪些保留
```

**3. 灵活性高**
```python
# 可以处理任意维度的张量
# 不需要手动reshape和permute
```

**4. 自动优化**
```python
# PyTorch会自动选择最优的计算路径
# 对于复杂运算，可能比手写更快
```

---

### 缺点 ❌

**1. 学习曲线**
```python
# 初学者需要时间理解符号含义
# 不如传统方法直观
```

**2. 调试困难**
```python
# 出错时，错误信息可能不够明确
# 'ijk,jkl->il' 写错了不容易发现
```

**3. 性能不稳定**
```python
# 简单操作可能比传统方法慢
# 需要测试才知道是否更快
```

**4. 不支持所有操作**
```python
# 只能表达线性代数运算
# 不能表达条件、循环等
```

---

## 七、使用建议

### 何时使用einsum？

**✅ 推荐使用：**
```python
# 1. 复杂的张量收缩
torch.einsum('bijk,bjkl->bil', A, B)

# 2. 多维批量运算
torch.einsum('bhqd,bhkd->bhqk', Q, K)

# 3. 需要清晰表达维度关系
torch.einsum('bni,bnj->bij', X, X)

# 4. 实现论文中的公式
# 论文：C_ij = Σ_k A_ik B_kj
torch.einsum('ik,kj->ij', A, B)
```

**❌ 不推荐使用：**
```python
# 1. 简单的矩阵乘法
A @ B  # 比 einsum('ik,kj->ij', A, B) 更清晰

# 2. 简单的求和
A.sum()  # 比 einsum('ij->', A) 更直观

# 3. 转置
A.T  # 比 einsum('ij->ji', A) 更简洁
```

---

### 性能优化建议

```python
# 1. 对于简单操作，传统方法可能更快
# 测试对比：
import time

A = torch.randn(1000, 1000)
B = torch.randn(1000, 1000)

# einsum
start = time.time()
result1 = torch.einsum('ik,kj->ij', A, B)
print(f"einsum: {time.time() - start:.6f}s")

# 传统
start = time.time()
result2 = A @ B
print(f"传统: {time.time() - start:.6f}s")

# 2. 使用opt_einsum库进一步优化
# pip install opt_einsum
import opt_einsum as oe

# 自动找到最优计算路径
result = oe.contract('ijk,jkl,lmn->imn', A, B, C, backend='torch')
```

---

## 八、常见错误

### 错误1：维度不匹配

```python
A = torch.randn(3, 4)
B = torch.randn(5, 6)

# 错误！
try:
    result = torch.einsum('ik,kj->ij', A, B)
except RuntimeError as e:
    print(f"错误: {e}")
    # k在A中是4，在B中是5，不匹配！

# 正确
B = torch.randn(4, 6)
result = torch.einsum('ik,kj->ij', A, B)  # ✓
```

---

### 错误2：字母重复使用不当

```python
A = torch.randn(3, 4)
B = torch.randn(3, 4)

# 错误：想做逐元素乘法，但写成了求和
result = torch.einsum('ij,ij->', A, B)
# 这会对所有元素求和！

# 正确
result = torch.einsum('ij,ij->ij', A, B)  # 逐元素乘法
```

---

### 错误3：忘记指定输出维度

```python
A = torch.randn(3, 4)

# 不指定输出
result = torch.einsum('ij', A)
# 等价于 'ij->ij'，返回原矩阵

# 如果想求和，需要明确指定
result = torch.einsum('ij->', A)  # 全部求和
```

---

## 九、总结

### 核心规则

```
1. 字母表示维度
   'ij' → 二维张量，i是第0维，j是第1维

2. 重复字母 = 求和
   'ik,kj' → k重复，对k求和

3. 输出只包含指定的字母
   'ik,kj->ij' → 输出只有i和j

4. 省略箭头 = 自动推断
   'ij' → 'ij->ij'（返回原张量）
```

---

### 常用模式速查

| 操作 | einsum | 形状示例 |
|------|--------|----------|
| 转置 | `'ij->ji'` | [3,4]→[4,3] |
| 求和 | `'ij->'` | [3,4]→[] |
| 按行求和 | `'ij->i'` | [3,4]→[3] |
| 对角线 | `'ii->i'` | [3,3]→[3] |
| 迹 | `'ii->'` | [3,3]→[] |
| 矩阵乘法 | `'ik,kj->ij'` | [3,4],[4,5]→[3,5] |
| 批量矩阵乘法 | `'bik,bkj->bij'` | [B,3,4],[B,4,5]→[B,3,5] |
| 点积 | `'i,i->'` | [3],[3]→[] |
| 外积 | `'i,j->ij'` | [3],[4]→[3,4] |
| 逐元素乘 | `'ij,ij->ij'` | [3,4],[3,4]→[3,4] |

---

### 记忆要点

```
einsum = "用字母描述张量运算"

规则：
1. 每个字母 = 一个维度
2. 重复字母 = 求和维度
3. 输出字母 = 保留维度
4. 逗号 = 分隔不同输入

例子：'bik,bkj->bij'
     ↓   ↓    ↓
     A   B    C
     
- b: batch（保留）
- i: 行（保留）
- j: 列（保留）
- k: 重复（求和）
```

**einsum是强大而优雅的张量运算工具！** 🎯