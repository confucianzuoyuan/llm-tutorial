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

# Parameters for 4 different scenarios
scenarios = [
    {'start': -0.5, 'lr': 0.1, 'max_iter': 8, 'title': 'Start = -0.5, LR = 0.1'},
    {'start': 2, 'lr': 0.1, 'max_iter': 5, 'title': 'Start = 2, LR = 0.1'},
    {'start': -0.5, 'lr': 0.3, 'max_iter': 101, 'title': 'Start = -0.5, LR = 0.3'},
    {'start': 2, 'lr': 0.3, 'max_iter': 3, 'title': 'Start = 2, LR = 0.3'}
]

# Create figure with 4 subplots
fig, axes = plt.subplots(1, 4, figsize=(20, 5))

# Plot range for the function (domain: -1 to 3)
x_range = np.linspace(-1, 3, 500)
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
    ax.plot(x_range, y_range, 'b-', linewidth=2.5, label='$f(x) = x^2 - 4x + 1$')
    
    # Plot gradient descent steps
    steps_y = [func1(x) for x in steps]
    ax.plot(steps, steps_y, 'r-', linewidth=2, alpha=0.7, label='Descent Path', zorder=4)
    ax.plot(steps, steps_y, 'ro', markersize=7, zorder=5)
    
    # Mark starting point
    ax.plot(steps[0], func1(steps[0]), 'go', markersize=13, 
            label=f'Start: x={steps[0]}', zorder=6, markeredgecolor='darkgreen', markeredgewidth=2)
    
    # Mark final point
    ax.plot(final_x, func1(final_x), 'r*', markersize=18, 
            label=f'Final: x={final_x:.4f}', zorder=6)
    
    # Add annotation for final result
    # Adjust annotation position based on scenario
    if scenario['start'] == 2:
        text_x = final_x + 0.3
        text_y = func1(final_x) + 1.5
    else:
        text_x = final_x + 0.5
        text_y = func1(final_x) + 2
    

    
    # Mark the true minimum
    true_min_x = 2  # Derivative = 0 at x = 2
    ax.axvline(x=true_min_x, color='green', linestyle='--', 
               linewidth=1.5, alpha=0.6, label='True Minimum (x=2)')
    
    # Labels and title
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.set_title(f"{scenario['title']}\n(Max Iter: {scenario['max_iter']})", 
                 fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=8, loc='upper right')
    ax.set_xlim(-1, 2.5)
    ax.set_ylim(0, 4)


plt.tight_layout()
plt.show()

# Print summary
print("Summary of Results:")
print("=" * 80)
for scenario in scenarios:
    steps, final_x = gradient_descent(
        start=scenario['start'],
        gradient=gradient_func1,
        learn_rate=scenario['lr'],
        max_iter=scenario['max_iter']
    )
    print(f"Start: {scenario['start']:>5} | LR: {scenario['lr']:.1f} | "
          f"Final x: {final_x:>8.6f} | f(x): {func1(final_x):>8.6f} | "
          f"Steps: {len(steps)-1:>3}")
