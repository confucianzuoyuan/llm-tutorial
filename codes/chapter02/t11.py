import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

np.random.seed(0)
x = np.random.rand(100, 1)
y = 5 + 2 * x + np.random.rand(100, 1)

# Initialize parameters
W = 0
b = 0

def predict(x, W, b):
    """Make predictions based on input x"""
    y = W * x + b
    return y

def mean_squared_error(x0, x1):
    """Calculate mean squared error"""
    diff = x0 - x1
    return np.sum(diff ** 2) / len(diff)

def compute_loss(x, y, W, b):
    """Compute loss for given W and b"""
    y_pred = predict(x, W, b)
    return mean_squared_error(y, y_pred)

def gradient(x, y, W, b):
    """Calculate gradients"""
    N = len(x)
    W_grad = 2 / N * sum((W * x_i[0] + b - y_i[0]) * x_i[0] for (x_i, y_i) in zip(x, y))
    b_grad = 2 / N * sum((W * x_i[0] + b - y_i[0]) for (x_i, y_i) in zip(x, y))
    return W_grad, b_grad

# ==================== Gradient Descent Training ====================
lr = 0.1
iters = 100

# Record training process
W_history = [W]
b_history = [b]
loss_history = []

W_current = W
b_current = b

for i in range(iters):
    y_pred = predict(x, W_current, b_current)
    loss = mean_squared_error(y, y_pred)
    loss_history.append(loss)
    
    W_grad, b_grad = gradient(x, y, W_current, b_current)
    W_current = W_current - lr * W_grad
    b_current = b_current - lr * b_grad
    
    W_history.append(W_current)
    b_history.append(b_current)
    
    if i < 10:
        print(f"Iter {i}: W={W_current:.4f}, b={b_current:.4f}, Loss={loss:.4f}")

print(f"\nFinal result: W={W_current:.4f}, b={b_current:.4f}")
print(f"True values:  W=2.0000, b=5.0000")

# ==================== Create Loss Surface ====================
# Create grid in reasonable range of W and b
W_range = np.linspace(-1, 4, 100)
b_range = np.linspace(3, 7, 100)
W_grid, b_grid = np.meshgrid(W_range, b_range)

# Calculate loss for each grid point
loss_grid = np.zeros_like(W_grid)
for i in range(W_grid.shape[0]):
    for j in range(W_grid.shape[1]):
        loss_grid[i, j] = compute_loss(x, y, W_grid[i, j], b_grid[i, j])

# ==================== Visualization ====================
fig = plt.figure(figsize=(18, 12))

# ========== 1. 3D Surface Plot ==========
ax1 = fig.add_subplot(2, 3, 1, projection='3d')
surf = ax1.plot_surface(W_grid, b_grid, loss_grid, 
                        cmap=cm.viridis, alpha=0.6, 
                        linewidth=0, antialiased=True)

# Plot gradient descent path (first 10 iterations)
ax1.plot(W_history[:11], b_history[:11], 
         [compute_loss(x, y, W_history[i], b_history[i]) for i in range(11)],
         'r.-', linewidth=2, markersize=8, label='Gradient Descent Path')

# Mark start and end points
ax1.scatter([W_history[0]], [b_history[0]], 
           [compute_loss(x, y, W_history[0], b_history[0])],
           color='green', s=100, marker='o', label='Start', zorder=5)
ax1.scatter([W_history[10]], [b_history[10]], 
           [compute_loss(x, y, W_history[10], b_history[10])],
           color='red', s=100, marker='*', label='Iter 10', zorder=5)

ax1.set_xlabel('W (Weight)', fontsize=11, fontweight='bold')
ax1.set_ylabel('b (Bias)', fontsize=11, fontweight='bold')
ax1.set_zlabel('Loss (MSE)', fontsize=11, fontweight='bold')
ax1.set_title('Loss Surface with Gradient Descent (First 10 Iterations)', 
              fontsize=12, fontweight='bold')
ax1.legend()
fig.colorbar(surf, ax=ax1, shrink=0.5, aspect=5)

# ========== 2. Contour Plot (First 10 iterations) ==========
ax2 = fig.add_subplot(2, 3, 2)
contour = ax2.contour(W_grid, b_grid, loss_grid, levels=30, cmap='viridis')
ax2.clabel(contour, inline=True, fontsize=8)

# Plot gradient descent path (first 10 iterations)
ax2.plot(W_history[:11], b_history[:11], 'r.-', 
         linewidth=2, markersize=10, label='Gradient Descent')

# Annotate each iteration point
for i in range(11):
    ax2.annotate(f'{i}', 
                xy=(W_history[i], b_history[i]),
                xytext=(5, 5), textcoords='offset points',
                fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

# Mark starting point
ax2.scatter([W_history[0]], [b_history[0]], 
           color='green', s=150, marker='o', 
           label='Start (W=0, b=0)', zorder=5, edgecolors='black', linewidths=2)

# Mark optimal point (true values)
ax2.scatter([2], [5], color='blue', s=150, marker='*', 
           label='True Optimum (W=2, b=5)', zorder=5, edgecolors='black', linewidths=2)

ax2.set_xlabel('W (Weight)', fontsize=11, fontweight='bold')
ax2.set_ylabel('b (Bias)', fontsize=11, fontweight='bold')
ax2.set_title('Loss Contour - First 10 Iterations', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)

# ========== 3. Contour Plot (All 100 iterations) ==========
ax3 = fig.add_subplot(2, 3, 3)
contour = ax3.contour(W_grid, b_grid, loss_grid, levels=30, cmap='viridis')
ax3.clabel(contour, inline=True, fontsize=8)

# Plot complete gradient descent path
ax3.plot(W_history, b_history, 'r.-', 
         linewidth=1.5, markersize=3, alpha=0.6, label='Full Path (100 iters)')

# Mark key points
key_iters = [0, 10, 50, 100]
colors = ['green', 'orange', 'purple', 'red']
for idx, i in enumerate(key_iters):
    ax3.scatter([W_history[i]], [b_history[i]], 
               color=colors[idx], s=100, marker='o', 
               label=f'Iter {i}', zorder=5, edgecolors='black', linewidths=1.5)

ax3.scatter([2], [5], color='blue', s=150, marker='*', 
           label='True Optimum', zorder=5, edgecolors='black', linewidths=2)

ax3.set_xlabel('W (Weight)', fontsize=11, fontweight='bold')
ax3.set_ylabel('b (Bias)', fontsize=11, fontweight='bold')
ax3.set_title('Loss Contour - All 100 Iterations', fontsize=12, fontweight='bold')
ax3.legend(loc='upper right', fontsize=9)
ax3.grid(True, alpha=0.3)

# ========== 4. Loss vs Iteration ==========
ax4 = fig.add_subplot(2, 3, 4)
ax4.plot(range(len(loss_history)), loss_history, 'b-', linewidth=2)
ax4.scatter(range(10), loss_history[:10], color='red', s=50, zorder=5, 
           label='First 10 iterations')
ax4.set_xlabel('Iteration', fontsize=11, fontweight='bold')
ax4.set_ylabel('Loss (MSE)', fontsize=11, fontweight='bold')
ax4.set_title('Loss vs Iteration', fontsize=12, fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.legend()

# ========== 5. Weight W vs Iteration ==========
ax5 = fig.add_subplot(2, 3, 5)
ax5.plot(range(len(W_history)), W_history, 'g-', linewidth=2, label='W')
ax5.axhline(y=2, color='r', linestyle='--', linewidth=2, label='True W=2')
ax5.scatter(range(11), W_history[:11], color='red', s=50, zorder=5)
ax5.set_xlabel('Iteration', fontsize=11, fontweight='bold')
ax5.set_ylabel('W (Weight)', fontsize=11, fontweight='bold')
ax5.set_title('Weight W vs Iteration', fontsize=12, fontweight='bold')
ax5.grid(True, alpha=0.3)
ax5.legend()

# ========== 6. Bias b vs Iteration ==========
ax6 = fig.add_subplot(2, 3, 6)
ax6.plot(range(len(b_history)), b_history, 'm-', linewidth=2, label='b')
ax6.axhline(y=5, color='r', linestyle='--', linewidth=2, label='True b=5')
ax6.scatter(range(11), b_history[:11], color='red', s=50, zorder=5)
ax6.set_xlabel('Iteration', fontsize=11, fontweight='bold')
ax6.set_ylabel('b (Bias)', fontsize=11, fontweight='bold')
ax6.set_title('Bias b vs Iteration', fontsize=12, fontweight='bold')
ax6.grid(True, alpha=0.3)
ax6.legend()

plt.tight_layout()
plt.show()

# ==================== Print First 10 Iterations Details ====================
print("\n" + "="*70)
print("First 10 Iterations - Detailed Information")
print("="*70)
print(f"{'Iter':<6} {'W':<12} {'b':<12} {'Loss':<12} {'Delta_W':<12} {'Delta_b':<12}")
print("-"*70)

for i in range(10):
    delta_W = W_history[i+1] - W_history[i]
    delta_b = b_history[i+1] - b_history[i]
    loss = compute_loss(x, y, W_history[i], b_history[i])
    print(f"{i:<6} {W_history[i]:<12.6f} {b_history[i]:<12.6f} "
          f"{loss:<12.6f} {delta_W:<12.6f} {delta_b:<12.6f}")

print("="*70)

# ==================== Animation-style Visualization ==========
fig2, axes = plt.subplots(2, 5, figsize=(20, 8))
fig2.suptitle('Gradient Descent Animation - First 10 Iterations', 
              fontsize=14, fontweight='bold')

for idx in range(10):
    ax = axes[idx // 5, idx % 5]
    
    # Draw contour lines
    contour = ax.contour(W_grid, b_grid, loss_grid, levels=20, 
                        cmap='viridis', alpha=0.6)
    
    # Draw path up to current iteration
    ax.plot(W_history[:idx+2], b_history[:idx+2], 'r.-', 
           linewidth=2, markersize=8)
    
    # Mark current point
    ax.scatter([W_history[idx+1]], [b_history[idx+1]], 
              color='red', s=200, marker='*', zorder=5,
              edgecolors='black', linewidths=2)
    
    # Mark starting point
    ax.scatter([W_history[0]], [b_history[0]], 
              color='green', s=100, marker='o', zorder=5,
              edgecolors='black', linewidths=2)
    
    # Mark true optimal point
    ax.scatter([2], [5], color='blue', s=100, marker='*', 
              zorder=5, edgecolors='black', linewidths=2)
    
    loss_current = compute_loss(x, y, W_history[idx+1], b_history[idx+1])
    ax.set_title(f'Iter {idx}\nW={W_history[idx+1]:.3f}, b={b_history[idx+1]:.3f}\nLoss={loss_current:.3f}',
                fontsize=10, fontweight='bold')
    ax.set_xlabel('W', fontsize=9)
    ax.set_ylabel('b', fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim([W_range[0], W_range[-1]])
    ax.set_ylim([b_range[0], b_range[-1]])

plt.tight_layout()
plt.show()

# ==================== Final Fitting Result ==========
fig3, ax = plt.subplots(1, 1, figsize=(10, 6))
ax.scatter(x, y, s=30, alpha=0.6, label='Training Data')
ax.plot(x, predict(x, W_current, b_current), 'r-', 
       linewidth=3, label=f'Fitted Line: y={W_current:.3f}x+{b_current:.3f}')
ax.plot(x, predict(x, 2, 5), 'g--', 
       linewidth=2, label='True Line: y=2x+5')
ax.set_xlabel('x', fontsize=12, fontweight='bold')
ax.set_ylabel('y', fontsize=12, fontweight='bold')
ax.set_title('Linear Regression Result', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
