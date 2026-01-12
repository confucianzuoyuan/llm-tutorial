import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Create mesh grid
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)

# Define the function f(x,y) = 0.5x^2 + y^2
Z = 0.5 * X**2 + Y**2

# Create figure with two subplots
fig = plt.figure(figsize=(14, 6))

# First subplot: 3D surface plot
ax1 = fig.add_subplot(121, projection='3d')
surf = ax1.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.9, edgecolor='none')

# Mark the minimum point at (0, 0, 0)
ax1.scatter([0], [0], [0], color='red', s=150, marker='o', 
            label='Minimum Point (0, 0, 0)', zorder=5)

# Add annotation
ax1.text(0, 0, 0.5, 'Minimum\n(0, 0, 0)', 
         fontsize=11, color='red', fontweight='bold',
         ha='center')

# Labels and title
ax1.set_xlabel('x', fontsize=12)
ax1.set_ylabel('y', fontsize=12)
ax1.set_zlabel('f(x, y)', fontsize=12)
ax1.set_title('3D Surface: $f(x,y) = 0.5x^2 + y^2$', fontsize=14)
ax1.legend(fontsize=10)

# Add colorbar
fig.colorbar(surf, ax=ax1, shrink=0.5, aspect=5)

# Set viewing angle
ax1.view_init(elev=25, azim=45)

# Second subplot: Contour plot
ax2 = fig.add_subplot(122)
contour = ax2.contour(X, Y, Z, levels=15, cmap='coolwarm')
contourf = ax2.contourf(X, Y, Z, levels=15, cmap='coolwarm', alpha=0.6)
ax2.clabel(contour, inline=True, fontsize=8)

# Mark minimum point
ax2.plot(0, 0, 'r*', markersize=20, label='Minimum (0, 0)', zorder=5)

# Add arrow annotation
ax2.annotate('Minimum Point', 
             xy=(0, 0),
             xytext=(0.8, 1.0),
             fontsize=11,
             color='red',
             fontweight='bold',
             arrowprops=dict(arrowstyle='->', 
                           color='red',
                           lw=2.5))

# Labels and title
ax2.set_xlabel('x', fontsize=12)
ax2.set_ylabel('y', fontsize=12)
ax2.set_title('Contour Plot: $f(x,y) = 0.5x^2 + y^2$', fontsize=14)
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=10)
ax2.set_aspect('equal')

# Add colorbar for contour plot
fig.colorbar(contourf, ax=ax2, shrink=0.8, aspect=10)

plt.tight_layout()
plt.show()
