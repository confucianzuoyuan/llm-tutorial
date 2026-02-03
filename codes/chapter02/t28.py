import torch
import torch.nn as nn
import matplotlib.pyplot as plt

# 超简单的注意力
class TinyAttention(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.W_q = nn.Linear(dim, dim, bias=False)
        self.W_k = nn.Linear(dim, dim, bias=False)
        self.W_v = nn.Linear(dim, dim, bias=False)
        
    def forward(self, x):
        Q = self.W_q(x)
        K = self.W_k(x)
        V = self.W_v(x)
        
        scores = Q @ K.T / (dim ** 0.5)
        weights = torch.softmax(scores, dim=-1)
        output = weights @ V
        
        return output, weights

# 训练
dim = 4
model = TinyAttention(dim)
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

# 简单数据
x = torch.randn(3, dim)  # 3个词
target = torch.randn(3, dim)

# 记录注意力
attention_history = []

for epoch in range(100):
    optimizer.zero_grad()
    output, weights = model(x)
    loss = ((output - target) ** 2).mean()
    loss.backward()
    optimizer.step()
    
    attention_history.append(weights.detach().numpy())
    
    if epoch % 20 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}")
        print("注意力权重:")
        print(weights.detach().numpy())
        print()

# 画图
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.imshow(attention_history[0], cmap='hot')
plt.title('initial attention')
plt.colorbar()

plt.subplot(1, 3, 2)
plt.imshow(attention_history[-1], cmap='hot')
plt.title('final attention')
plt.colorbar()

plt.subplot(1, 3, 3)
for i in range(3):
    plt.plot([a[i, 0] for a in attention_history], label=f'Query{i}→Key0')
plt.legend()
plt.title('attention change')
plt.xlabel('epoch')
plt.ylabel('attention weights')

plt.tight_layout()
plt.show()
