import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(18, 10))

# ========== 1. Convex Function Example ==========
ax1 = plt.subplot(2, 4, 1)

x = np.linspace(-2, 3, 300)
f_convex = x**2  # Convex function

ax1.plot(x, f_convex, 'b-', linewidth=3, label='f(x) = x² (Convex)')

# Choose two points
x1, x2 = -1, 2
y1, y2 = x1**2, x2**2

# Plot points
ax1.plot([x1, x2], [y1, y2], 'ro', markersize=12, zorder=5, label='Endpoints')

# Plot the line segment (chord)
ax1.plot([x1, x2], [y1, y2], 'r--', linewidth=2.5, alpha=0.7, label='Chord')

# Show several intermediate points
lambdas = [0.2, 0.4, 0.5, 0.6, 0.8]
for lam in lambdas:
    x_mid = lam * x1 + (1-lam) * x2
    f_mid = x_mid**2
    y_chord = lam * y1 + (1-lam) * y2
    
    # Point on function
    ax1.plot(x_mid, f_mid, 'go', markersize=8, zorder=4)
    # Point on chord
    ax1.plot(x_mid, y_chord, 'rs', markersize=8, zorder=4, alpha=0.6)
    # Vertical line showing inequality
    ax1.plot([x_mid, x_mid], [f_mid, y_chord], 'g-', linewidth=1.5, alpha=0.5)
    
    if lam == 0.5:
        ax1.annotate('', xy=(x_mid, y_chord), xytext=(x_mid, f_mid),
                    arrowprops=dict(arrowstyle='<->', color='green', lw=2))
        ax1.text(x_mid+0.2, (f_mid+y_chord)/2, 
                'f(λx+(1-λ)y) ≤\nλf(x)+(1-λ)f(y)', 
                fontsize=9, color='green', weight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax1.set_xlabel('x', fontsize=12)
ax1.set_ylabel('f(x)', fontsize=12)
ax1.set_title('Convex Function Example: f(x) = x²', fontsize=12, weight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10, loc='upper center')
ax1.set_ylim(-0.5, 5)

# ========== 2. Concave Function Example ==========
ax2 = plt.subplot(2, 4, 2)

f_concave = -x**2  # Concave function

ax2.plot(x, f_concave, 'r-', linewidth=3, label='f(x) = -x² (Concave)')

y1_concave, y2_concave = -x1**2, -x2**2
ax2.plot([x1, x2], [y1_concave, y2_concave], 'bo', markersize=12, zorder=5, label='Endpoints')
ax2.plot([x1, x2], [y1_concave, y2_concave], 'b--', linewidth=2.5, alpha=0.7, label='Chord')

for lam in lambdas:
    x_mid = lam * x1 + (1-lam) * x2
    f_mid = -x_mid**2
    y_chord = lam * y1_concave + (1-lam) * y2_concave
    
    ax2.plot(x_mid, f_mid, 'mo', markersize=8, zorder=4)
    ax2.plot(x_mid, y_chord, 'bs', markersize=8, zorder=4, alpha=0.6)
    ax2.plot([x_mid, x_mid], [f_mid, y_chord], 'm-', linewidth=1.5, alpha=0.5)
    
    if lam == 0.5:
        ax2.annotate('', xy=(x_mid, f_mid), xytext=(x_mid, y_chord),
                    arrowprops=dict(arrowstyle='<->', color='magenta', lw=2))
        ax2.text(x_mid+0.2, (f_mid+y_chord)/2, 
                'f(λx+(1-λ)y) ≥\nλf(x)+(1-λ)f(y)', 
                fontsize=9, color='magenta', weight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax2.set_xlabel('x', fontsize=12)
ax2.set_ylabel('f(x)', fontsize=12)
ax2.set_title('Concave Function Example: f(x) = -x²', fontsize=12, weight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=10, loc='lower center')
ax2.set_ylim(-5, 0.5)

# ========== 3. Common Convex Functions ==========
ax3 = plt.subplot(2, 4, 3)

x_pos = np.linspace(0.1, 3, 300)
ax3.plot(x_pos, x_pos**2, 'b-', linewidth=2.5, label='x²')
ax3.plot(x_pos, np.exp(x_pos), 'r-', linewidth=2.5, label='eˣ')
ax3.plot(x_pos, -np.log(x_pos), 'g-', linewidth=2.5, label='-ln(x)')
ax3.plot(x_pos, np.abs(x_pos), 'm-', linewidth=2.5, label='|x|')

ax3.set_xlabel('x', fontsize=12)
ax3.set_ylabel('f(x)', fontsize=12)
ax3.set_title('Common Convex Functions', fontsize=12, weight='bold')
ax3.grid(True, alpha=0.3)
ax3.legend(fontsize=10)
ax3.set_ylim(0, 10)

# ========== 4. Non-convex Function ==========
ax4 = plt.subplot(2, 4, 4)

x_range = np.linspace(-2, 3, 300)
f_nonconvex = np.sin(2*x_range) + 0.5*x_range  # Non-convex

ax4.plot(x_range, f_nonconvex, 'purple', linewidth=3, label='f(x) = sin(2x) + 0.5x')

# Show violation of convexity
x1_nc, x2_nc = -1, 2.5
y1_nc = np.sin(2*x1_nc) + 0.5*x1_nc
y2_nc = np.sin(2*x2_nc) + 0.5*x2_nc

ax4.plot([x1_nc, x2_nc], [y1_nc, y2_nc], 'ro', markersize=12, zorder=5)
ax4.plot([x1_nc, x2_nc], [y1_nc, y2_nc], 'r--', linewidth=2.5, alpha=0.7)

lam = 0.5
x_mid = lam * x1_nc + (1-lam) * x2_nc
f_mid = np.sin(2*x_mid) + 0.5*x_mid
y_chord = lam * y1_nc + (1-lam) * y2_nc

ax4.plot(x_mid, f_mid, 'go', markersize=10, zorder=4)
ax4.plot(x_mid, y_chord, 'rs', markersize=10, zorder=4)
ax4.plot([x_mid, x_mid], [min(f_mid, y_chord), max(f_mid, y_chord)], 
        'orange', linewidth=2, alpha=0.7)

ax4.text(x_mid+0.3, (f_mid+y_chord)/2, 
        'Violates\nconvexity!', 
        fontsize=10, color='orange', weight='bold',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax4.set_xlabel('x', fontsize=12)
ax4.set_ylabel('f(x)', fontsize=12)
ax4.set_title('Non-convex Function Example', fontsize=12, weight='bold')
ax4.grid(True, alpha=0.3)
ax4.legend(fontsize=10)

# ========== 5. Strictly Convex ==========
ax5 = plt.subplot(2, 4, 5)

x_strict = np.linspace(-2, 2, 300)
f_strict = x_strict**2 + 0.1*x_strict**4  # Strictly convex

ax5.plot(x_strict, f_strict, 'darkblue', linewidth=3, label='Strictly Convex')

x1_s, x2_s = -1.5, 1.5
y1_s = x1_s**2 + 0.1*x1_s**4
y2_s = x2_s**2 + 0.1*x2_s**4

ax5.plot([x1_s, x2_s], [y1_s, y2_s], 'ro', markersize=12, zorder=5)
ax5.plot([x1_s, x2_s], [y1_s, y2_s], 'r--', linewidth=2.5, alpha=0.7)

# Fill the area between chord and function
x_fill = np.linspace(x1_s, x2_s, 100)
f_fill = x_fill**2 + 0.1*x_fill**4
y_chord_fill = y1_s + (y2_s - y1_s) * (x_fill - x1_s) / (x2_s - x1_s)
ax5.fill_between(x_fill, f_fill, y_chord_fill, alpha=0.3, color='green', 
                 label='Strict inequality region')

ax5.text(0, 3.5, 'f(λx+(1-λ)y) < λf(x)+(1-λ)f(y)\nfor all λ∈(0,1)', 
        fontsize=9, ha='center', weight='bold',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

ax5.set_xlabel('x', fontsize=12)
ax5.set_ylabel('f(x)', fontsize=12)
ax5.set_title('Strictly Convex Function', fontsize=12, weight='bold')
ax5.grid(True, alpha=0.3)
ax5.legend(fontsize=9, loc='upper center')

# ========== 6. First Order Condition ==========
ax6 = plt.subplot(2, 4, 6)

x_foc = np.linspace(-2, 3, 300)
f_foc = x_foc**2

ax6.plot(x_foc, f_foc, 'b-', linewidth=3, label='f(x) = x²')

# Point x
x_point = 1
f_point = x_point**2
grad_point = 2*x_point  # Gradient at x

ax6.plot(x_point, f_point, 'ro', markersize=12, zorder=5, label=f'Point x={x_point}')

# Tangent line (first order approximation)
tangent_x = np.linspace(-1, 3, 100)
tangent_y = f_point + grad_point * (tangent_x - x_point)
ax6.plot(tangent_x, tangent_y, 'r--', linewidth=2.5, alpha=0.7, 
        label='Tangent line')

# Show that function is above tangent
y_test = 2.5
f_test = y_test**2
tangent_test = f_point + grad_point * (y_test - x_point)

ax6.plot(y_test, f_test, 'go', markersize=10, zorder=4)
ax6.plot(y_test, tangent_test, 'gs', markersize=10, zorder=4, alpha=0.6)
ax6.plot([y_test, y_test], [tangent_test, f_test], 'g-', linewidth=2)

ax6.annotate('', xy=(y_test, f_test), xytext=(y_test, tangent_test),
            arrowprops=dict(arrowstyle='<->', color='green', lw=2))
ax6.text(y_test+0.2, (f_test+tangent_test)/2, 
        'f(y) ≥ f(x) +\n∇f(x)ᵀ(y-x)', 
        fontsize=9, color='green', weight='bold',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax6.set_xlabel('x', fontsize=12)
ax6.set_ylabel('f(x)', fontsize=12)
ax6.set_title('First-Order Condition', fontsize=12, weight='bold')
ax6.grid(True, alpha=0.3)
ax6.legend(fontsize=9)
ax6.set_ylim(-1, 10)

# ========== 7. Second Order Condition ==========
ax7 = plt.subplot(2, 4, 7)

# Show Hessian visualization
x_hess = np.linspace(-2, 2, 300)
f_hess = x_hess**2
f_hess_second = 2 * np.ones_like(x_hess)  # Second derivative

ax7_twin = ax7.twinx()

ax7.plot(x_hess, f_hess, 'b-', linewidth=3, label='f(x) = x²')
ax7_twin.plot(x_hess, f_hess_second, 'r--', linewidth=2.5, label="f''(x) = 2 > 0")
ax7_twin.axhline(y=0, color='k', linewidth=1, linestyle=':', alpha=0.5)

ax7.set_xlabel('x', fontsize=12)
ax7.set_ylabel('f(x)', fontsize=12, color='b')
ax7_twin.set_ylabel("f''(x)", fontsize=12, color='r')
ax7.set_title('Second-Order Condition\n(Hessian ≥ 0)', fontsize=12, weight='bold')
ax7.grid(True, alpha=0.3)
ax7.tick_params(axis='y', labelcolor='b')
ax7_twin.tick_params(axis='y', labelcolor='r')

# Add text box
ax7.text(0, 3, "Convex ⟺ f''(x) ≥ 0\n(Hessian PSD)", 
        fontsize=10, ha='center', weight='bold',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

lines1, labels1 = ax7.get_legend_handles_labels()
lines2, labels2 = ax7_twin.get_legend_handles_labels()
ax7.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc='upper left')

# ========== 8. 2D Convex Function ==========
ax8 = plt.subplot(2, 4, 8, projection='3d')

x_2d = np.linspace(-2, 2, 50)
y_2d = np.linspace(-2, 2, 50)
X, Y = np.meshgrid(x_2d, y_2d)
Z = X**2 + Y**2  # Convex function

ax8.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7, edgecolor='none')

# Mark two points
x1_3d, y1_3d = -1, -1
x2_3d, y2_3d = 1, 1
z1_3d = x1_3d**2 + y1_3d**2
z2_3d = x2_3d**2 + y2_3d**2

ax8.scatter([x1_3d, x2_3d], [y1_3d, y2_3d], [z1_3d, z2_3d], 
           color='red', s=100, zorder=5)

# Line segment between points
ax8.plot([x1_3d, x2_3d], [y1_3d, y2_3d], [z1_3d, z2_3d], 
        'r--', linewidth=3, alpha=0.8, label='Chord')

# Add some intermediate points
for lam in [0.25, 0.5, 0.75]:
    x_mid = lam * x1_3d + (1-lam) * x2_3d
    y_mid = lam * y1_3d + (1-lam) * y2_3d
    z_mid = x_mid**2 + y_mid**2
    z_chord = lam * z1_3d + (1-lam) * z2_3d
    ax8.scatter([x_mid], [y_mid], [z_mid], color='green', s=50, zorder=4)
    ax8.plot([x_mid, x_mid], [y_mid, y_mid], [z_mid, z_chord], 'g-', linewidth=2, alpha=0.6)

ax8.set_xlabel('x', fontsize=10)
ax8.set_ylabel('y', fontsize=10)
ax8.set_zlabel('f(x,y)', fontsize=10)
ax8.set_title('Bivariate Convex Function\nf(x,y) = x² + y²', fontsize=11, weight='bold')
ax8.view_init(elev=20, azim=45)

plt.tight_layout()
plt.show()
