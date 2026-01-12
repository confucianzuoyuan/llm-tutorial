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
    return x ** 2 - 4 * x + 1

def gradient_func1(x: float):
    return 2 * x - 4

# Parameters for 4 different scenarios
scenarios = [
    {'start': 9, 'lr': 0.1, 'max_iter': 24, 'title': 'Learning Rate = 0.1'},
    {'start': 9, 'lr': 0.3, 'max_iter': 8, 'title': 'Learning Rate = 0.3'},
    {'start': 9, 'lr': 0.8, 'max_iter': 15, 'title': 'Learning Rate = 0.8'},
    {'start': 9, 'lr': 0.9, 'max_iter': 33, 'title': 'Learning Rate = 0.9'}
]

# Create figure with 4 subplots
fig, axes = plt.subplots(1, 4, figsize=(20, 5))

# Plot range for the function (domain: -10 to 10)
x_range = np.linspace(-6, 10, 500)
y_range = func1(x_range)

for idx, (ax, scenario) in enumerate(zip(axes, scenarios)):
    # Run gradient descent
    steps, final_x = gradient_descent(
        start=scenario['start'],
        gradient=gradient_func1,
        learn_rate=scenario['lr'],
        max_iter=scenario['max_iter']
    )
    
    # Plot the function
    ax.plot(x_range, y_range, 'b-', linewidth=2, label='$f(x) = x^2 - 4x + 1$')
    
    # Plot gradient descent steps
    steps_y = [func1(x) for x in steps]
    ax.plot(steps, steps_y, 'ro-', linewidth=1.5, markersize=6, 
            label=f'Gradient Descent Path', zorder=5)
    
    # Mark starting point
    ax.plot(steps[0], func1(steps[0]), 'go', markersize=12, 
            label=f'Start: x={steps[0]}', zorder=6)
    
    # Mark final point
    ax.plot(final_x, func1(final_x), 'g*', markersize=15, 
            label=f'Final: x={final_x:.4f}', zorder=6)
    
    # Add annotation for final result
    # Adjust annotation position based on final_x location
    if final_x < 0:
        text_x = final_x + 3
        text_y = func1(final_x) + 20
    else:
        text_x = final_x - 3
        text_y = func1(final_x) + 20
    
    ax.annotate(f'Final x = {final_x:.4f}\nf(x) = {func1(final_x):.4f}\nSteps: {len(steps)-1}', 
                xy=(final_x, func1(final_x)),
                xytext=(text_x, text_y),
                fontsize=9,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
    
    # Mark the true minimum
    true_min_x = 2  # Derivative = 0 at x = 2
    ax.axvline(x=true_min_x, color='green', linestyle='--', 
               linewidth=1, alpha=0.5, label='True Minimum (x=2)')
    
    # Labels and title
    ax.set_xlabel('x', fontsize=11)
    ax.set_ylabel('f(x)', fontsize=11)
    ax.set_title(f"{scenario['title']}\n(Max Iter: {scenario['max_iter']})", 
                 fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, loc='upper center')
    ax.set_xlim(-6, 10)
    ax.set_ylim(-5, 60)

plt.tight_layout()
plt.show()

# Print summary
print("Summary of Results:")
print("=" * 70)
for scenario in scenarios:
    steps, final_x = gradient_descent(
        start=scenario['start'],
        gradient=gradient_func1,
        learn_rate=scenario['lr'],
        max_iter=scenario['max_iter']
    )
    print(f"Learning Rate: {scenario['lr']:.1f} | "
          f"Final x: {final_x:.6f} | "
          f"f(x): {func1(final_x):.6f} | "
          f"Steps: {len(steps)-1}")
