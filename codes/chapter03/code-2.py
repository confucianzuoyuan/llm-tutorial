import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(14, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# 定义颜色
color_input = '#E8F4F8'
color_hidden = '#FFF4E6'
color_output = '#E8F5E9'
color_activation = '#FFE5E5'

# 输入层
input_box = FancyBboxPatch((0.5, 3), 1.5, 4, 
                           boxstyle="round,pad=0.1", 
                           edgecolor='#2196F3', facecolor=color_input, linewidth=2)
ax.add_patch(input_box)
ax.text(1.25, 5, 'Input Layer\n(X)', ha='center', va='center', 
        fontsize=12, fontweight='bold')
ax.text(1.25, 4.2, 'Shape:\n(784, m)', ha='center', va='center', 
        fontsize=9, style='italic')

# 第一层计算 (z1 = w1·X + b1)
calc1_box = FancyBboxPatch((2.5, 3.5), 1.5, 3, 
                          boxstyle="round,pad=0.1", 
                          edgecolor='#FF9800', facecolor='#FFF3E0', linewidth=2)
ax.add_patch(calc1_box)
ax.text(3.25, 5.5, 'z₁ = w₁·X + b₁', ha='center', va='center', 
        fontsize=11, fontweight='bold')
ax.text(3.25, 4.5, 'w₁: (n₁, 784)\nb₁: (n₁, 1)', ha='center', va='center', 
        fontsize=8, style='italic')

# ReLU激活
relu_box = FancyBboxPatch((2.5, 1.5), 1.5, 1.5, 
                         boxstyle="round,pad=0.1", 
                         edgecolor='#F44336', facecolor=color_activation, linewidth=2)
ax.add_patch(relu_box)
ax.text(3.25, 2.25, 'ReLU(z₁)', ha='center', va='center', 
        fontsize=11, fontweight='bold')

# 隐藏层
hidden_box = FancyBboxPatch((4.5, 3), 1.5, 4, 
                           boxstyle="round,pad=0.1", 
                           edgecolor='#FF9800', facecolor=color_hidden, linewidth=2)
ax.add_patch(hidden_box)
ax.text(5.25, 5, 'Hidden Layer\n(a₁)', ha='center', va='center', 
        fontsize=12, fontweight='bold')
ax.text(5.25, 4.2, 'Shape:\n(n₁, m)', ha='center', va='center', 
        fontsize=9, style='italic')

# 第二层计算 (z2 = w2·a1 + b2)
calc2_box = FancyBboxPatch((6.5, 3.5), 1.5, 3, 
                          boxstyle="round,pad=0.1", 
                          edgecolor='#4CAF50', facecolor='#F1F8E9', linewidth=2)
ax.add_patch(calc2_box)
ax.text(7.25, 5.5, 'z₂ = w₂·a₁ + b₂', ha='center', va='center', 
        fontsize=11, fontweight='bold')
ax.text(7.25, 4.5, 'w₂: (10, n₁)\nb₂: (10, 1)', ha='center', va='center', 
        fontsize=8, style='italic')

# Softmax激活
softmax_box = FancyBboxPatch((6.5, 1.5), 1.5, 1.5, 
                            boxstyle="round,pad=0.1", 
                            edgecolor='#F44336', facecolor=color_activation, linewidth=2)
ax.add_patch(softmax_box)
ax.text(7.25, 2.25, 'Softmax(z₂)', ha='center', va='center', 
        fontsize=11, fontweight='bold')

# 输出层
output_box = FancyBboxPatch((8.5, 3), 1.5, 4, 
                           boxstyle="round,pad=0.1", 
                           edgecolor='#4CAF50', facecolor=color_output, linewidth=2)
ax.add_patch(output_box)
ax.text(9.25, 5, 'Output Layer\n(a₂)', ha='center', va='center', 
        fontsize=12, fontweight='bold')
ax.text(9.25, 4.2, 'Shape:\n(10, m)', ha='center', va='center', 
        fontsize=9, style='italic')
ax.text(9.25, 3.5, 'Probabilities\nfor 0-9', ha='center', va='center', 
        fontsize=8, style='italic')

# 绘制箭头
arrow_props = dict(arrowstyle='->', lw=2.5, color='#424242')

# X -> z1
ax.annotate('', xy=(2.5, 5), xytext=(2, 5), arrowprops=arrow_props)

# z1 -> ReLU
ax.annotate('', xy=(3.25, 3.5), xytext=(3.25, 3), 
            arrowprops=dict(arrowstyle='->', lw=2, color='#F44336'))

# ReLU -> a1
ax.annotate('', xy=(4.5, 2.25), xytext=(4, 2.25), 
            arrowprops=dict(arrowstyle='->', lw=2, color='#F44336'))
ax.annotate('', xy=(4.5, 5), xytext=(4.5, 2.5), 
            arrowprops=dict(arrowstyle='->', lw=1.5, color='#666666', linestyle='dashed'))

# a1 -> z2
ax.annotate('', xy=(6.5, 5), xytext=(6, 5), arrowprops=arrow_props)

# z2 -> Softmax
ax.annotate('', xy=(7.25, 3.5), xytext=(7.25, 3), 
            arrowprops=dict(arrowstyle='->', lw=2, color='#F44336'))

# Softmax -> a2
ax.annotate('', xy=(8.5, 2.25), xytext=(8, 2.25), 
            arrowprops=dict(arrowstyle='->', lw=2, color='#F44336'))
ax.annotate('', xy=(8.5, 5), xytext=(8.5, 2.5), 
            arrowprops=dict(arrowstyle='->', lw=1.5, color='#666666', linestyle='dashed'))

# 添加标题
ax.text(5, 8.5, 'Two-Layer Neural Network Architecture', 
        ha='center', va='center', fontsize=16, fontweight='bold')

# 添加图例
legend_elements = [
    mpatches.Patch(facecolor=color_input, edgecolor='#2196F3', label='Input'),
    mpatches.Patch(facecolor=color_hidden, edgecolor='#FF9800', label='Hidden'),
    mpatches.Patch(facecolor=color_output, edgecolor='#4CAF50', label='Output'),
    mpatches.Patch(facecolor=color_activation, edgecolor='#F44336', label='Activation')
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

# 添加注释
ax.text(5, 0.5, 'm = batch size (number of training examples)', 
        ha='center', va='center', fontsize=9, style='italic', color='#666')

plt.tight_layout()
plt.show()
