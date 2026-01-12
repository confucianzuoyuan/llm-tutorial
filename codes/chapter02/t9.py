import numpy as np
import matplotlib.pyplot as plt
from typing import Callable

def gradient_descent(start: float, gradient: Callable[[float], float],
                     learn_rate: float, max_iter: int, tol: float = 0.01):
    x = start
    steps = [start]  # 历史跟踪

    for _ in range(max_iter):
        diff = learn_rate * gradient(x)
        if np.abs(diff) < tol:
            break
        x = x - diff
        steps.append(x)  # 历史跟踪

    return steps, x

def func1(x: float):
    return x ** 4 - 2 * x ** 3 + 2

def gradient_func1(x: float):
    return 4 * x ** 3 - 6 * x ** 2

# Single scenario parameters
start_point = -0.5
learning_rate = 0.4
max_iterations = 8

# Run gradient descent
steps, final_x = gradient_descent(
    start=start_point,
    gradient=gradient_func1,
    learn_rate=learning_rate,
    max_iter=max_iterations
)

# Create single plot
fig, ax = plt.subplots(1, 1, figsize=(12, 8))

# Plot range for the function
x_range = np.linspace(-1, 2.5, 500)
y_range = func1(x_range)

# Plot the function
ax.plot(x_range, y_range, 'b-', linewidth=3, label='$f(x) = x^4 - 2x^3 + 2$')

# Plot gradient descent steps
steps_y = [func1(x) for x in steps]
ax.plot(steps, steps_y, 'r-', linewidth=2.5, alpha=0.7, label='Descent Path', zorder=4)

# Plot each step with numbered markers
for i, (x, y) in enumerate(zip(steps, steps_y)):
    # Plot the point
    ax.plot(x, y, 'ro', markersize=10, zorder=5)
    
    # Add step number annotation
    ax.annotate(f'{i}', 
                xy=(x, y),
                xytext=(x + 0.08, y + 0.15),
                fontsize=11,
                fontweight='bold',
                color='darkred',
                bbox=dict(boxstyle='circle,pad=0.3', 
                         facecolor='white', 
                         edgecolor='red',
                         linewidth=1.5),
                zorder=6)

# Mark starting point with special style
ax.plot(steps[0], func1(steps[0]), 'go', markersize=15, 
        label=f'Start: x={steps[0]}', zorder=7, 
        markeredgecolor='darkgreen', markeredgewidth=2.5)

# Mark final point with special style
ax.plot(final_x, func1(final_x), 'r*', markersize=22, 
        label=f'Final: x={final_x:.4f}', zorder=7)

# Add annotation for final result
ax.annotate(f'Final Result:\nx = {final_x:.6f}\nf(x) = {func1(final_x):.6f}\nTotal Steps: {len(steps)-1}', 
            xy=(final_x, func1(final_x)),
            xytext=(final_x + 0.4, func1(final_x) + 0.8),
            fontsize=11,
            bbox=dict(boxstyle='round,pad=0.6', 
                     facecolor='yellow', 
                     alpha=0.85, 
                     edgecolor='orange',
                     linewidth=2),
            arrowprops=dict(arrowstyle='->', 
                          color='red', 
                          lw=2.5,
                          connectionstyle='arc3,rad=0.3'))

# Mark the true minimum at x = 1.5
true_min_x = 1.5  # Derivative = 0 at x = 1.5
ax.axvline(x=true_min_x, color='green', linestyle='--', 
           linewidth=2, alpha=0.6, label=f'Local Minimum (x=1.5)')

# Labels and title
ax.set_xlabel('x', fontsize=14, fontweight='bold')
ax.set_ylabel('f(x)', fontsize=14, fontweight='bold')
ax.set_title(f'Gradient Descent Visualization\n$f(x) = x^4 - 2x^3 + 2$\n' + 
             f'Start = {start_point}, Learning Rate = {learning_rate}, Max Iterations = {max_iterations}', 
             fontsize=15, fontweight='bold', pad=20)
ax.grid(True, alpha=0.4, linestyle='--', linewidth=0.8)
ax.legend(fontsize=11, loc='upper right', framealpha=0.9)
ax.set_xlim(-1, 2.5)
ax.set_ylim(0, 4)

plt.tight_layout()
plt.show()

# Print detailed summary
print("=" * 80)
print("Gradient Descent Summary")
print("=" * 80)
print(f"Function: f(x) = x^4 - 2x^3 + 2")
print(f"Starting Point: x = {start_point}")
print(f"Learning Rate: {learning_rate}")
print(f"Max Iterations: {max_iterations}")
print(f"Final Point: x = {final_x:.6f}")
print(f"Final Value: f(x) = {func1(final_x):.6f}")
print(f"Total Steps: {len(steps)-1}")
print("=" * 80)
print("\nStep-by-Step Details:")
print("-" * 80)
print(f"{'Step':<6} {'x':<15} {'f(x)':<15} {'Gradient':<15}")
print("-" * 80)
for i, x in enumerate(steps):
    print(f"{i:<6} {x:<15.6f} {func1(x):<15.6f} {gradient_func1(x):<15.6f}")
print("=" * 80)
