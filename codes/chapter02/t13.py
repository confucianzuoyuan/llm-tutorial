import numpy as np
import matplotlib.pyplot as plt

# Generate one period of sine wave
x = np.linspace(0, 2*np.pi, 1000)
y = np.sin(x)

# Choose a point for the tangent line (e.g., x = π/3)
x0 = np.pi / 3
y0 = np.sin(x0)

# Calculate the derivative (slope) at x0
# For sin(x), the derivative is cos(x)
slope = np.cos(x0)

# Generate tangent line: y - y0 = slope * (x - x0)
# We'll draw it over a range around x0
x_tangent = np.linspace(x0 - 1, x0 + 1, 100)
y_tangent = y0 + slope * (x_tangent - x0)

# Create the plot
plt.figure(figsize=(10, 6))

# Plot sine curve in black
plt.plot(x, y, 'k-', linewidth=2, label='sin(x)')

# Plot tangent line in red
plt.plot(x_tangent, y_tangent, 'r-', linewidth=2, label=f'Tangent at x={x0:.2f}')

# Mark the point of tangency
plt.plot(x0, y0, 'ro', markersize=8, label=f'Point ({x0:.2f}, {y0:.2f})')

# Add grid and labels
plt.grid(True, alpha=0.3)
plt.xlabel('x', fontsize=12)
plt.ylabel('y', fontsize=12)
plt.title('Sine Wave with Tangent Line', fontsize=14)
plt.legend(fontsize=10)

# Set axis limits
plt.xlim(0, 2*np.pi)
plt.ylim(-1.5, 1.5)

# Add x-axis labels with π notation
plt.xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi], 
           ['0', 'π/2', 'π', '3π/2', '2π'])

plt.tight_layout()
plt.show()
