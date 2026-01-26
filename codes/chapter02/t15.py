import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the function
def f(x, y):
    return x**2 + x*y + y**2

# Create a grid of x and y values
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

# Create figure with two subplots
fig = plt.figure(figsize=(16, 6))

# ========== 3D Surface Plot ==========
ax1 = fig.add_subplot(121, projection='3d')

# Plot the surface
surf = ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.9, 
                        edgecolor='none', antialiased=True)

# Add contour lines on the surface
ax1.contour(X, Y, Z, levels=15, colors='white', linewidths=0.5, alpha=0.5)

# Labels and title
ax1.set_xlabel('x', fontsize=12, labelpad=10)
ax1.set_ylabel('y', fontsize=12, labelpad=10)
ax1.set_zlabel('f(x, y)', fontsize=12, labelpad=10)
ax1.set_title('3D Surface Plot: f(x, y) = x² + xy + y²', fontsize=14, weight='bold', pad=20)

# Add colorbar
fig.colorbar(surf, ax=ax1, shrink=0.5, aspect=5)

# Set viewing angle
ax1.view_init(elev=25, azim=45)

# ========== Contour Plot ==========
ax2 = fig.add_subplot(122)

# Create filled contour plot
contourf = ax2.contourf(X, Y, Z, levels=20, cmap='viridis', alpha=0.8)

# Add contour lines with labels
contour = ax2.contour(X, Y, Z, levels=15, colors='black', linewidths=0.8, alpha=0.6)
ax2.clabel(contour, inline=True, fontsize=8, fmt='%.1f')

# Mark the minimum point (0, 0)
ax2.plot(0, 0, 'r*', markersize=15, label='Minimum (0, 0)', zorder=5)

# Labels and title
ax2.set_xlabel('x', fontsize=12)
ax2.set_ylabel('y', fontsize=12)
ax2.set_title('Contour Plot: f(x, y) = x² + xy + y²', fontsize=14, weight='bold')
ax2.set_aspect('equal')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=10)

# Add colorbar
fig.colorbar(contourf, ax=ax2, label='f(x, y)')

plt.tight_layout()
plt.show()
