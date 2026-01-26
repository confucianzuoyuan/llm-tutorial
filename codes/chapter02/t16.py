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

# Create figure
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# Create surface
x_surf = np.linspace(-1, 2.5, 60)
y_surf = np.linspace(-1, 2.5, 60)
X, Y = np.meshgrid(x_surf, y_surf)
Z = f(X, Y)

# Plot surface with transparency
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.3, 
                        edgecolor='none', antialiased=True)

# Add contour lines on the bottom
ax.contour(X, Y, Z, levels=10, offset=0, colors='gray', 
          linewidths=0.5, alpha=0.3, linestyles='solid')

# Point (x0, y0)
x0, y0 = 1.0, 0.5

# Direction vector (arbitrary direction)
alpha = np.pi / 6  # angle with x-axis
beta = np.pi / 2 - alpha  # angle with y-axis

# Direction unit vector length for visualization
direction_length = 1.2
dx_dir = direction_length * np.cos(alpha)
dy_dir = direction_length * np.sin(alpha)

# Small displacement along direction l
delta_l = 0.7
delta_x = delta_l * np.cos(alpha)
delta_y = delta_l * np.sin(alpha)

# New point
x1 = x0 + delta_x
y1 = y0 + delta_y

# Calculate function values
z0 = f(x0, y0)
z1 = f(x1, y1)

# ========== Plot points on surface ==========
ax.scatter([x0], [y0], [z0], color='red', s=150, zorder=10, 
          edgecolors='darkred', linewidths=2, label='(x₀, y₀, f(x₀,y₀))')
ax.scatter([x1], [y1], [z1], color='blue', s=120, zorder=10, 
          edgecolors='darkblue', linewidths=2, label='(x₀+Δx, y₀+Δy, f(x₀+Δx,y₀+Δy))')

# ========== Plot points on xy-plane (z=0) ==========
ax.scatter([x0], [y0], [0], color='red', s=100, zorder=5, alpha=0.6, marker='o')
ax.scatter([x1], [y1], [0], color='blue', s=80, zorder=5, alpha=0.6, marker='o')

# ========== Draw vertical lines from xy-plane to surface ==========
ax.plot([x0, x0], [y0, y0], [0, z0], 'r--', linewidth=2, alpha=0.5)
ax.plot([x1, x1], [y1, y1], [0, z1], 'b--', linewidth=2, alpha=0.5)

# ========== Draw direction vector l on xy-plane ==========
arrow_l = Arrow3D([x0, x0+dx_dir], [y0, y0+dy_dir], [0, 0], 
                  mutation_scale=25, lw=3, arrowstyle='-|>', 
                  color='green', alpha=0.8)
ax.add_artist(arrow_l)
ax.text(x0+dx_dir+0.1, y0+dy_dir, 0.1, 'Direction l', 
       fontsize=11, color='green', weight='bold')

# ========== Draw displacement Δl on xy-plane ==========
arrow_delta = Arrow3D([x0, x1], [y0, y1], [0, 0],
                      mutation_scale=20, lw=2.5, arrowstyle='-|>', 
                      color='purple', linestyle='--', alpha=0.9)
ax.add_artist(arrow_delta)
ax.text((x0+x1)/2-0.1, (y0+y1)/2, 0.15, 'Δl', 
       fontsize=12, color='purple', weight='bold')

# ========== Draw Δx component on xy-plane ==========
ax.plot([x0, x1], [y0, y0], [0, 0], 'b-', linewidth=2.5, alpha=0.7)
arrow_dx = Arrow3D([x0, x1], [y0, y0], [0, 0],
                   mutation_scale=15, lw=2, arrowstyle='<->', 
                   color='blue', alpha=0.8)
ax.add_artist(arrow_dx)
ax.text((x0+x1)/2, y0-0.15, 0, 'Δx', fontsize=11, color='blue', weight='bold')

# ========== Draw Δy component on xy-plane ==========
ax.plot([x1, x1], [y0, y1], [0, 0], 'b-', linewidth=2.5, alpha=0.7)
arrow_dy = Arrow3D([x1, x1], [y0, y1], [0, 0],
                   mutation_scale=15, lw=2, arrowstyle='<->', 
                   color='blue', alpha=0.8)
ax.add_artist(arrow_dy)
ax.text(x1+0.15, (y0+y1)/2, 0, 'Δy', fontsize=11, color='blue', weight='bold')

# ========== Draw path on surface ==========
# Create a smooth path along the direction
t_path = np.linspace(0, 1, 50)
x_path = x0 + delta_x * t_path
y_path = y0 + delta_y * t_path
z_path = f(x_path, y_path)
ax.plot(x_path, y_path, z_path, 'r-', linewidth=3.5, alpha=0.9, 
       label='Path on surface', zorder=8)

# ========== Draw Δf (change in function value) ==========
ax.plot([x1, x1], [y1, y1], [z0, z1], color='orange', 
       linewidth=3, linestyle='--', alpha=0.9)
arrow_df = Arrow3D([x1, x1], [y1, y1], [z0, z1],
                   mutation_scale=20, lw=2.5, arrowstyle='<->', 
                   color='orange', alpha=0.9)
ax.add_artist(arrow_df)
mid_z = (z0 + z1) / 2
ax.text(x1+0.2, y1+0.1, mid_z, 'Δf', fontsize=12, 
       color='orange', weight='bold')

# ========== Draw angle α on xy-plane ==========
# Create arc for angle
angle_radius = 0.25
angle_t = np.linspace(0, alpha, 30)
arc_x = x0 + angle_radius * np.cos(angle_t)
arc_y = y0 + angle_radius * np.sin(angle_t)
arc_z = np.zeros_like(arc_x)
ax.plot(arc_x, arc_y, arc_z, 'r-', linewidth=2.5, alpha=0.8)
ax.text(x0+0.35, y0+0.08, 0, 'α', fontsize=13, color='red', weight='bold')

# ========== Draw coordinate axes on xy-plane ==========
axis_length = 2.5
arrow_x = Arrow3D([0, axis_length], [0, 0], [0, 0],
                  mutation_scale=20, lw=1.5, arrowstyle='-|>', 
                  color='black', alpha=0.4)
ax.add_artist(arrow_x)
ax.text(axis_length+0.1, 0, 0, 'x', fontsize=12, weight='bold')

arrow_y = Arrow3D([0, 0], [0, axis_length], [0, 0],
                  mutation_scale=20, lw=1.5, arrowstyle='-|>', 
                  color='black', alpha=0.4)
ax.add_artist(arrow_y)
ax.text(0, axis_length+0.1, 0, 'y', fontsize=12, weight='bold')

# ========== Labels and formatting ==========
ax.set_xlabel('x', fontsize=12, labelpad=10)
ax.set_ylabel('y', fontsize=12, labelpad=10)
ax.set_zlabel('f(x, y)', fontsize=12, labelpad=10)

title = 'Directional Derivative: f(x, y) = x² + xy + y²\n'
title += r"$\frac{\partial f}{\partial l}(x_0, y_0) = \lim_{\Delta l \to 0} \frac{f(x_0 + \Delta x, y_0 + \Delta y) - f(x_0, y_0)}{\Delta l}$"
ax.set_title(title, fontsize=13, weight='bold', pad=25)

# Set viewing angle
ax.view_init(elev=25, azim=130)

# Set axis limits
ax.set_xlim(-0.5, 2.5)
ax.set_ylim(-0.5, 2.5)
ax.set_zlim(0, max(Z.max(), z1) + 1)

# Add legend
ax.legend(fontsize=10, loc='upper left')

# Add text box with formulas
formula_text = r'$\Delta x = \Delta l \cdot \cos\alpha$' + '\n' + r'$\Delta y = \Delta l \cdot \cos\beta$'
ax.text2D(0.02, 0.15, formula_text, transform=ax.transAxes, fontsize=11,
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
         verticalalignment='top')

# Add colorbar
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, pad=0.1)

plt.tight_layout()
plt.show()
