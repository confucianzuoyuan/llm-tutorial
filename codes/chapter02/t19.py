import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(18, 10))

x = np.linspace(-6, 6, 1000)

# Define activation functions
sigmoid = 1 / (1 + np.exp(-x))
relu = np.maximum(0, x)
tanh = np.tanh(x)

# Define derivatives
sigmoid_deriv = sigmoid * (1 - sigmoid)
relu_deriv = (x > 0).astype(float)
tanh_deriv = 1 - tanh**2

# ========== Row 1: Function Plots ==========
# Sigmoid Plot
ax1 = plt.subplot(2, 3, 1)
ax1.plot(x, sigmoid, 'b-', linewidth=4, label='σ(x)')
ax1.axhline(y=0, color='k', linewidth=0.5, alpha=0.3)
ax1.axhline(y=1, color='r', linewidth=1.5, linestyle='--', alpha=0.5)
ax1.axhline(y=0, color='r', linewidth=1.5, linestyle='--', alpha=0.5)
ax1.axvline(x=0, color='k', linewidth=0.5, alpha=0.3)
ax1.plot(0, 0.5, 'ro', markersize=12, zorder=5)

# Shade saturation regions
ax1.fill_between(x, 0, sigmoid, where=(x < -3), alpha=0.2, color='red')
ax1.fill_between(x, sigmoid, 1, where=(x > 3), alpha=0.2, color='red')

# Add formula
ax1.text(0.5, 0.15, r'$\sigma(x) = \frac{1}{1 + e^{-x}}$', 
        fontsize=16, weight='bold',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='blue', linewidth=2))

ax1.set_xlabel('x', fontsize=14, weight='bold')
ax1.set_ylabel('σ(x)', fontsize=14, weight='bold')
ax1.set_title('Sigmoid Function\nRange: (0, 1)', fontsize=14, weight='bold')
ax1.grid(True, alpha=0.3, linewidth=1.5)
ax1.set_ylim(-0.2, 1.2)
ax1.set_xlim(-6, 6)

# ReLU Plot
ax2 = plt.subplot(2, 3, 2)
ax2.plot(x, relu, 'g-', linewidth=4, label='ReLU(x)')
ax2.axhline(y=0, color='k', linewidth=0.5, alpha=0.3)
ax2.axvline(x=0, color='r', linewidth=2, linestyle='--', alpha=0.7)
ax2.plot(0, 0, 'ro', markersize=12, zorder=5)

# Shade regions
ax2.fill_between(x, 0, 0, where=(x < 0), alpha=0.3, color='red')
ax2.fill_between(x, 0, relu, where=(x > 0), alpha=0.2, color='green')

# Add formula
ax2.text(1, 1, r'$\mathrm{ReLU}(x) = \max(0, x)$', 
        fontsize=16, weight='bold',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='green', linewidth=2))

ax2.set_xlabel('x', fontsize=14, weight='bold')
ax2.set_ylabel('ReLU(x)', fontsize=14, weight='bold')
ax2.set_title('ReLU Function\nRange: [0, ∞)', fontsize=14, weight='bold')
ax2.grid(True, alpha=0.3, linewidth=1.5)
ax2.set_ylim(-1, 6)
ax2.set_xlim(-6, 6)

# Tanh Plot
ax3 = plt.subplot(2, 3, 3)
ax3.plot(x, tanh, 'orange', linewidth=4, label='tanh(x)')
ax3.axhline(y=0, color='k', linewidth=1, linestyle='-', alpha=0.5)
ax3.axhline(y=1, color='r', linewidth=1.5, linestyle='--', alpha=0.5)
ax3.axhline(y=-1, color='r', linewidth=1.5, linestyle='--', alpha=0.5)
ax3.axvline(x=0, color='k', linewidth=0.5, alpha=0.3)
ax3.plot(0, 0, 'ro', markersize=12, zorder=5)

# Shade saturation regions
ax3.fill_between(x, -1, tanh, where=(x < -3), alpha=0.2, color='red')
ax3.fill_between(x, tanh, 1, where=(x > 3), alpha=0.2, color='red')

# Add formula
ax3.text(0.5, -0.6, r'$\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$', 
        fontsize=16, weight='bold',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='orange', linewidth=2))

ax3.set_xlabel('x', fontsize=14, weight='bold')
ax3.set_ylabel('tanh(x)', fontsize=14, weight='bold')
ax3.set_title('Tanh Function\nRange: (-1, 1)', fontsize=14, weight='bold')
ax3.grid(True, alpha=0.3, linewidth=1.5)
ax3.set_ylim(-1.2, 1.2)
ax3.set_xlim(-6, 6)

# ========== Row 2: Derivative Plots ==========
# Sigmoid Derivative
ax4 = plt.subplot(2, 3, 4)
ax4.plot(x, sigmoid, 'b--', linewidth=2, alpha=0.4, label='σ(x)')
ax4_twin = ax4.twinx()
ax4_twin.plot(x, sigmoid_deriv, 'r-', linewidth=4, label="σ'(x)")
ax4_twin.plot(0, 0.25, 'ro', markersize=12, zorder=5)

# Shade vanishing gradient regions
ax4_twin.fill_between(x, 0, sigmoid_deriv, where=(np.abs(x) > 3), 
                      alpha=0.3, color='red')

# Add derivative formula
ax4_twin.text(0.5, 0.18, r"$\sigma'(x) = \sigma(x)(1-\sigma(x))$", 
        fontsize=14, weight='bold',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='red', linewidth=2))

ax4.set_xlabel('x', fontsize=14, weight='bold')
ax4.set_ylabel('σ(x)', fontsize=13, color='b')
ax4_twin.set_ylabel("σ'(x)", fontsize=13, color='r', weight='bold')
ax4.set_title("Sigmoid Derivative\nMax gradient: 0.25", fontsize=13, weight='bold')
ax4.grid(True, alpha=0.3, linewidth=1.5)
ax4.tick_params(axis='y', labelcolor='b')
ax4_twin.tick_params(axis='y', labelcolor='r')
ax4_twin.set_ylim(0, 0.3)

# ReLU Derivative
ax5 = plt.subplot(2, 3, 5)
ax5.plot(x, relu, 'g--', linewidth=2, alpha=0.4, label='ReLU(x)')
ax5_twin = ax5.twinx()
ax5_twin.plot(x, relu_deriv, 'r-', linewidth=4, label="ReLU'(x)")
ax5_twin.axvline(x=0, color='orange', linewidth=3, linestyle='--', alpha=0.7)

# Shade regions
ax5_twin.fill_between(x, 0, 1, where=(x > 0), alpha=0.3, color='green')
ax5_twin.fill_between(x, 0, 0, where=(x < 0), alpha=0.3, color='red')

# Add derivative formula - using text instead of cases
formula_text = "ReLU'(x) = 1  if x > 0\n           0  if x ≤ 0"
ax5_twin.text(1, 0.5, formula_text, 
        fontsize=13, weight='bold', family='monospace',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='red', linewidth=2))

ax5.set_xlabel('x', fontsize=14, weight='bold')
ax5.set_ylabel('ReLU(x)', fontsize=13, color='g')
ax5_twin.set_ylabel("ReLU'(x)", fontsize=13, color='r', weight='bold')
ax5.set_title("ReLU Derivative\nGradient: 0 or 1", fontsize=13, weight='bold')
ax5.grid(True, alpha=0.3, linewidth=1.5)
ax5.tick_params(axis='y', labelcolor='g')
ax5_twin.tick_params(axis='y', labelcolor='r')
ax5_twin.set_ylim(-0.2, 1.5)

# Tanh Derivative
ax6 = plt.subplot(2, 3, 6)
ax6.plot(x, tanh, 'orange', linewidth=2, alpha=0.4, linestyle='--', label='tanh(x)')
ax6_twin = ax6.twinx()
ax6_twin.plot(x, tanh_deriv, 'r-', linewidth=4, label="tanh'(x)")
ax6_twin.plot(0, 1, 'ro', markersize=12, zorder=5)

# Shade vanishing gradient regions
ax6_twin.fill_between(x, 0, tanh_deriv, where=(np.abs(x) > 3), 
                      alpha=0.3, color='red')

# Add derivative formula
ax6_twin.text(0.5, 0.7, r"$\tanh'(x) = 1 - \tanh^2(x)$", 
        fontsize=14, weight='bold',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='red', linewidth=2))

ax6.set_xlabel('x', fontsize=14, weight='bold')
ax6.set_ylabel('tanh(x)', fontsize=13, color='orange')
ax6_twin.set_ylabel("tanh'(x)", fontsize=13, color='r', weight='bold')
ax6.set_title("Tanh Derivative\nMax gradient: 1", fontsize=13, weight='bold')
ax6.grid(True, alpha=0.3, linewidth=1.5)
ax6.tick_params(axis='y', labelcolor='orange')
ax6_twin.tick_params(axis='y', labelcolor='r')
ax6_twin.set_ylim(0, 1.2)

plt.tight_layout()
plt.show()
