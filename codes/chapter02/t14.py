import numpy as np
import matplotlib.pyplot as plt

# Define the function (sine wave)
def f(x):
    return np.sin(x)

# Choose a point x0
x0 = np.pi / 3
y0 = f(x0)

# Choose a delta x for visualization
delta_x = 0.8

# Calculate the corresponding point
x1 = x0 + delta_x
y1 = f(x1)

# Generate the curve
x = np.linspace(0, 2*np.pi, 1000)
y = f(x)

# Calculate the derivative (slope) at x0
slope = np.cos(x0)

# Generate tangent line
x_tangent = np.linspace(x0 - 0.5, x0 + 1.5, 100)
y_tangent = y0 + slope * (x_tangent - x0)

# Generate secant line (connecting the two points)
x_secant = np.linspace(x0 - 0.2, x1 + 0.2, 100)
secant_slope = (y1 - y0) / delta_x
y_secant = y0 + secant_slope * (x_secant - x0)

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the curve in black
ax.plot(x, y, 'k-', linewidth=2.5, label='f(x) = sin(x)')

# Plot the secant line in blue
ax.plot(x_secant, y_secant, 'b--', linewidth=2, label='Secant line', alpha=0.7)

# Plot the tangent line in red
ax.plot(x_tangent, y_tangent, 'r-', linewidth=2, label="Tangent line (f'(x₀))")

# Mark the two points
ax.plot(x0, y0, 'ro', markersize=10, zorder=5)
ax.plot(x1, y1, 'bo', markersize=10, zorder=5)

# Draw vertical and horizontal lines to show Δx and Δy
ax.plot([x0, x1], [y0, y0], 'g--', linewidth=1.5, alpha=0.6)
ax.plot([x1, x1], [y0, y1], 'g--', linewidth=1.5, alpha=0.6)

# Add annotations
ax.annotate('', xy=(x1, y0), xytext=(x0, y0),
            arrowprops=dict(arrowstyle='<->', color='green', lw=2))
ax.text((x0 + x1) / 2, y0 - 0.15, 'Δx', fontsize=14, ha='center', color='green', weight='bold')

ax.annotate('', xy=(x1, y1), xytext=(x1, y0),
            arrowprops=dict(arrowstyle='<->', color='green', lw=2))
ax.text(x1 + 0.15, (y0 + y1) / 2, 'Δy', fontsize=14, ha='left', color='green', weight='bold')

# Label the points
ax.text(x0 - 0.1, y0 + 0.15, f'(x₀, f(x₀))', fontsize=12, ha='right', weight='bold')
ax.text(x1 + 0.1, y1 + 0.15, f'(x₀+Δx, f(x₀+Δx))', fontsize=12, ha='left', weight='bold')

# Add title and formula
ax.set_title("Derivative as the Limit of Difference Quotient", fontsize=16, weight='bold', pad=20)
formula_text = r"$f'(x_0) = \lim_{\Delta x \to 0} \frac{\Delta y}{\Delta x} = \lim_{\Delta x \to 0} \frac{f(x_0 + \Delta x) - f(x_0)}{\Delta x}$"
ax.text(0.5, 0.98, formula_text, transform=ax.transAxes, 
        fontsize=14, ha='center', va='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Add grid and labels
ax.grid(True, alpha=0.3)
ax.set_xlabel('x', fontsize=13)
ax.set_ylabel('y', fontsize=13)
ax.legend(fontsize=11, loc='lower left')

# Set axis limits
ax.set_xlim(-0.2, 2*np.pi)
ax.set_ylim(-1.3, 1.5)

# Add x-axis labels with π notation
ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])

plt.tight_layout()
plt.show()
