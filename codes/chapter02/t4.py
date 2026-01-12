import matplotlib.pyplot as plt
import numpy as np

# Create x values in the domain (-1, 3)
x = np.linspace(-1, 3, 1000)

# Define the function f(x) = x^4 - 2x^3 + 2
y = x**4 - 2*x**3 + 2

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2, label='$f(x) = x^4 - 2x^3 + 2$')

# Mark the saddle point at (0, 2)
plt.plot(0, 2, 'ro', markersize=10, label='Saddle Point (0, 2)')

# Add arrow annotation pointing to the saddle point
plt.annotate('saddle point', 
             xy=(0, 2),  # Point to annotate
             xytext=(0.8, 3.5),  # Position of the text
             fontsize=12,
             arrowprops=dict(arrowstyle='->', 
                           connectionstyle='arc3,rad=0.3',
                           color='red',
                           lw=2),
             bbox=dict(boxstyle='round,pad=0.5', 
                      facecolor='yellow', 
                      alpha=0.7))

# Add labels and title
plt.xlabel('x', fontsize=12)
plt.ylabel('f(x)', fontsize=12)
plt.title('Graph of $f(x) = x^4 - 2x^3 + 2$', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)

# Set axis limits for better visualization
plt.xlim(-1, 3)
plt.ylim(-1, 5)

# Add axes through origin
plt.axhline(y=0, color='k', linewidth=0.5)
plt.axvline(x=0, color='k', linewidth=0.5)

plt.tight_layout()
plt.show()
