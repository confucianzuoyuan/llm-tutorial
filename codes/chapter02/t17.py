import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        return np.min(zs)

# Define the function
def f(x, y):
    return x**2 + x*y + y**2

# Partial derivatives
def df_dx(x, y):
    return 2*x + y

def df_dy(x, y):
    return x + 2*y

# Create figure with two subplots
fig = plt.figure(figsize=(16, 7))

# ========== Left: 2D Contour Plot with Gradient Vectors ==========
ax1 = fig.add_subplot(121)

# Create grid
x = np.linspace(-2, 3, 100)
y = np.linspace(-2, 3, 100)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

# Plot filled contours
contourf = ax1.contourf(X, Y, Z, levels=20, cmap='viridis', alpha=0.6)
contour = ax1.contour(X, Y, Z, levels=15, colors='black', linewidths=0.8, alpha=0.4)
ax1.clabel(contour, inline=True, fontsize=8, fmt='%.1f')

# Point of interest
x0, y0 = 1.0, 1.0
z0 = f(x0, y0)

# Calculate gradient at (1, 1)
grad_x = df_dx(x0, y0)
grad_y = df_dy(x0, y0)

# Plot the point
ax1.plot(x0, y0, 'ro', markersize=15, zorder=10, 
        markeredgecolor='darkred', markeredgewidth=2, label=f'Point (1, 1)')

# Plot gradient vector (scaled for visibility)
scale = 0.3
ax1.arrow(x0, y0, scale*grad_x, scale*grad_y, 
         head_width=0.15, head_length=0.2, fc='red', ec='red', 
         linewidth=3, alpha=0.9, zorder=8, length_includes_head=True)
ax1.text(x0 + scale*grad_x + 0.3, y0 + scale*grad_y + 0.2, 
        f'∇f(1,1) = ({grad_x}, {grad_y})', 
        fontsize=13, color='red', weight='bold',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Plot partial derivative components
# ∂f/∂x component (horizontal)
ax1.arrow(x0, y0, scale*grad_x, 0, 
         head_width=0.12, head_length=0.15, fc='blue', ec='blue', 
         linewidth=2, alpha=0.7, zorder=7, linestyle='--')
ax1.text(x0 + scale*grad_x/2, y0 - 0.3, 
        f'∂f/∂x = {grad_x}', fontsize=11, color='blue', weight='bold')

# ∂f/∂y component (vertical)
ax1.arrow(x0, y0, 0, scale*grad_y, 
         head_width=0.12, head_length=0.15, fc='green', ec='green', 
         linewidth=2, alpha=0.7, zorder=7, linestyle='--')
ax1.text(x0 - 0.5, y0 + scale*grad_y/2, 
        f'∂f/∂y = {grad_y}', fontsize=11, color='green', weight='bold')

# Add several gradient vectors at different points
sample_points = [(0, 0), (1.5, 0.5), (-0.5, 1.5), (0.5, -0.5)]
for px, py in sample_points:
    gx = df_dx(px, py)
    gy = df_dy(px, py)
    ax1.arrow(px, py, scale*gx, scale*gy, 
             head_width=0.1, head_length=0.15, fc='orange', ec='orange', 
             linewidth=1.5, alpha=0.6, zorder=6)

# Labels and formatting
ax1.set_xlabel('x', fontsize=13)
ax1.set_ylabel('y', fontsize=13)
ax1.set_title('Gradient Vector Field on Contour Plot\nf(x, y) = x² + xy + y²', 
             fontsize=13, weight='bold', pad=15)
ax1.set_aspect('equal')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=11, loc='upper left')

# Add colorbar
cbar = fig.colorbar(contourf, ax=ax1)
cbar.set_label('f(x, y)', fontsize=11)

# Add formula (fixed LaTeX syntax)
formula_text = '∇f(1,1) = (∂f/∂x, ∂f/∂y) = (3, 3)'
ax1.text(0.05, 0.95, formula_text, transform=ax1.transAxes, fontsize=11,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

# ========== Right: 3D Surface with Gradient ==========
ax2 = fig.add_subplot(122, projection='3d')

# Create surface
x_surf = np.linspace(-2, 3, 60)
y_surf = np.linspace(-2, 3, 60)
X_surf, Y_surf = np.meshgrid(x_surf, y_surf)
Z_surf = f(X_surf, Y_surf)

# Plot surface
surf = ax2.plot_surface(X_surf, Y_surf, Z_surf, cmap='viridis', 
                        alpha=0.4, edgecolor='none', antialiased=True)

# Add contours on bottom
ax2.contour(X_surf, Y_surf, Z_surf, levels=15, offset=0, 
           colors='gray', linewidths=0.5, alpha=0.3)

# Plot the point on surface
ax2.scatter([x0], [y0], [z0], color='red', s=200, zorder=10,
           edgecolors='darkred', linewidths=2, label=f'Point (1, 1, {z0})')

# Plot point on xy-plane
ax2.scatter([x0], [y0], [0], color='red', s=100, zorder=5, alpha=0.5)

# Vertical line from xy-plane to surface
ax2.plot([x0, x0], [y0, y0], [0, z0], 'r--', linewidth=2, alpha=0.5)

# Plot gradient vector on xy-plane
arrow_grad = Arrow3D([x0, x0+scale*grad_x], [y0, y0+scale*grad_y], [0, 0],
                     mutation_scale=25, lw=3.5, arrowstyle='-|>', 
                     color='red', alpha=0.9)
ax2.add_artist(arrow_grad)

# Plot gradient vector at surface level
arrow_grad_surf = Arrow3D([x0, x0+scale*grad_x], [y0, y0+scale*grad_y], [z0, z0],
                          mutation_scale=25, lw=3.5, arrowstyle='-|>', 
                          color='red', alpha=0.9)
ax2.add_artist(arrow_grad_surf)

# Plot partial derivative components on xy-plane
arrow_dx = Arrow3D([x0, x0+scale*grad_x], [y0, y0], [0, 0],
                   mutation_scale=20, lw=2.5, arrowstyle='-|>', 
                   color='blue', linestyle='--', alpha=0.7)
ax2.add_artist(arrow_dx)

arrow_dy = Arrow3D([x0, x0], [y0, y0+scale*grad_y], [0, 0],
                   mutation_scale=20, lw=2.5, arrowstyle='-|>', 
                   color='green', linestyle='--', alpha=0.7)
ax2.add_artist(arrow_dy)

# Add labels
ax2.text(x0+scale*grad_x+0.2, y0+scale*grad_y+0.2, z0+0.5, 
        '∇f(1,1)', fontsize=12, color='red', weight='bold')
ax2.text(x0+scale*grad_x/2, y0-0.3, 0, 
        '∂f/∂x', fontsize=10, color='blue', weight='bold')
ax2.text(x0-0.3, y0+scale*grad_y/2, 0, 
        '∂f/∂y', fontsize=10, color='green', weight='bold')

# Draw a path in the gradient direction on surface
t_path = np.linspace(0, 0.5, 30)
x_path = x0 + scale*grad_x*t_path
y_path = y0 + scale*grad_y*t_path
z_path = f(x_path, y_path)
ax2.plot(x_path, y_path, z_path, 'r-', linewidth=3, alpha=0.8, 
        label='Steepest ascent direction')

# Labels and formatting
ax2.set_xlabel('x', fontsize=12, labelpad=10)
ax2.set_ylabel('y', fontsize=12, labelpad=10)
ax2.set_zlabel('f(x, y)', fontsize=12, labelpad=10)
ax2.set_title('Gradient on 3D Surface\nf(x, y) = x² + xy + y²', 
             fontsize=13, weight='bold', pad=20)

# Set viewing angle
ax2.view_init(elev=25, azim=135)

# Set limits
ax2.set_xlim(-2, 3)
ax2.set_ylim(-2, 3)
ax2.set_zlim(0, Z_surf.max())

ax2.legend(fontsize=10, loc='upper left')

# Add main formula at bottom (fixed LaTeX syntax)
formula_main = '∇f(x,y) = (∂f/∂x, ∂f/∂y) = (2x+y, x+2y)'
fig.text(0.5, 0.02, formula_main, ha='center', fontsize=13,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))

plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.show()
