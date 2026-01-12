import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Create mesh grid
x = np.linspace(-1, 1, 100)
y = np.linspace(-1, 1, 100)
X, Y = np.meshgrid(x, y)

# Define the function z = x^2 - y^2
Z = X**2 - Y**2

# Create 3D plot
fig = plt.figure(figsize=(12, 5))

# First subplot: 3D surface plot
ax1 = fig.add_subplot(121, projection='3d')
surf = ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8, edgecolor='none')

# Mark the saddle point at (0, 0, 0)
ax1.scatter([0], [0], [0], color='red', s=100, marker='o', label='Saddle Point (0, 0, 0)')

# Add annotation for saddle point
ax1.text(0, 0, 0.3, 'Saddle Point\n(0, 0, 0)', 
         fontsize=11, color='red', fontweight='bold',
         ha='center')

# Labels and title
ax1.set_xlabel('x', fontsize=11)
ax1.set_ylabel('y', fontsize=11)
ax1.set_zlabel('z', fontsize=11)
ax1.set_title('3D Surface: $z = x^2 - y^2$', fontsize=13)
ax1.legend()

# Add colorbar
fig.colorbar(surf, ax=ax1, shrink=0.5, aspect=5)

# Second subplot: Contour plot
ax2 = fig.add_subplot(122)
contour = ax2.contour(X, Y, Z, levels=20, cmap='viridis')
ax2.clabel(contour, inline=True, fontsize=8)

# Mark saddle point on contour plot
ax2.plot(0, 0, 'ro', markersize=10, label='Saddle Point (0, 0)')

# Add arrow annotation
ax2.annotate('Saddle Point', 
             xy=(0, 0),
             xytext=(0.4, 0.5),
             fontsize=11,
             color='red',
             fontweight='bold',
             arrowprops=dict(arrowstyle='->', 
                           color='red',
                           lw=2))

# Labels and title
ax2.set_xlabel('x', fontsize=11)
ax2.set_ylabel('y', fontsize=11)
ax2.set_title('Contour Plot: $z = x^2 - y^2$', fontsize=13)
ax2.grid(True, alpha=0.3)
ax2.legend()
ax2.set_aspect('equal')

plt.tight_layout()
plt.show()
