import torch
import torch.nn as nn

# 设置随机种子以便复现
torch.manual_seed(42)

# 定义参数
vocab_size = 2
embedding_dim = 2
input_ids = torch.tensor([0, 1, 0])

# 创建嵌入层
embedding = nn.Embedding(vocab_size, embedding_dim)

# 查看初始权重
print("初始嵌入矩阵 W:")
print(embedding.weight)
print()

# 前向传播
output = embedding(input_ids)
print("嵌入输出 E:")
print(output)
print()

# 假设一个简单的损失：所有元素的平方和
loss = (output ** 2).sum()
print(f"损失 L = {loss.item():.4f}")
print()

# 反向传播
loss.backward()

# 查看梯度
print("嵌入矩阵的梯度 ∂L/∂W:")
print(embedding.weight.grad)
print()

# 手动计算验证
print("=== 手动验证 ===")
# ∂L/∂E = 2 * E（因为 L = sum(E²)）
grad_E = 2 * output
print("∂L/∂E (梯度矩阵 G):")
print(grad_E)
print()

# 手动计算 ∂L/∂W
grad_W_manual = torch.zeros(vocab_size, embedding_dim)
for i, idx in enumerate(input_ids):
    grad_W_manual[idx] += grad_E[i]

print("手动计算的 ∂L/∂W:")
print(grad_W_manual)
print()

# 验证是否一致
print("PyTorch 梯度与手动计算是否一致:")
print(torch.allclose(embedding.weight.grad, grad_W_manual))
