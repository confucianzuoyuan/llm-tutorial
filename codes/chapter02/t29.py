import numpy as np
import matplotlib.pyplot as plt

def get_positional_encoding(max_len, d_model):
    """
    生成位置编码
    
    参数：
    max_len: 最大序列长度（比如10个词）
    d_model: 编码维度（比如每个位置用4个数字表示）
    """
    # 创建一个空矩阵，用来存放位置编码
    pe = np.zeros((max_len, d_model))
    
    # 对每个位置
    for pos in range(max_len):
        # 对每个维度
        for i in range(0, d_model, 2):
            # 计算频率（波的快慢）
            freq = 1.0 / (10000 ** (i / d_model))
            
            # 偶数维度用正弦
            pe[pos, i] = np.sin(pos * freq)
            
            # 奇数维度用余弦
            if i + 1 < d_model:
                pe[pos, i + 1] = np.cos(pos * freq)
    
    return pe

# 生成位置编码
max_len = 10  # 10个位置
d_model = 4   # 每个位置用4个数字

pe = get_positional_encoding(max_len, d_model)

print("位置编码矩阵：")
print(pe)
print("\n每一行代表一个位置的编码")
print("每一列代表一个维度")

import matplotlib.pyplot as plt

# 生成更多位置的编码
max_len = 500
d_model = 128
pe = get_positional_encoding(max_len, d_model)

# 画图
plt.figure(figsize=(12, 6))
plt.imshow(pe.T, cmap='RdBu', aspect='auto')
plt.colorbar(label='encoding value')
plt.xlabel('position')
plt.ylabel('dim')
plt.title('like footprint')
plt.show()
