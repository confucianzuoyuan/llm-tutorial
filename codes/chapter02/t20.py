import numpy as np
import matplotlib.pyplot as plt

# ========== Example 1: The Dilemma of Step Size Selection ==========
print("=" * 60)
print("Example 1: Step Size Selection Problem in Numerical Differentiation")
print("=" * 60)

def f(x):
    """Test function: f(x) = sin(x)"""
    return np.sin(x)

def f_derivative_exact(x):
    """Exact derivative: f'(x) = cos(x)"""
    return np.cos(x)

def numerical_derivative(f, x, h):
    """Numerical differentiation using central difference"""
    return (f(x + h) - f(x - h)) / (2 * h)

# Test point
x0 = 1.0
exact_deriv = f_derivative_exact(x0)

print(f"\nAt x = {x0}:")
print(f"Exact derivative: {exact_deriv:.15f}")
print("\nNumerical derivatives with different step sizes:")
print("-" * 60)
print(f"{'Step size h':<15} {'Numerical derivative':<20} {'Absolute error':<20}")
print("-" * 60)

# Test different step sizes
h_values = [1e-1, 1e-2, 1e-4, 1e-8, 1e-12, 1e-16]
errors = []

for h in h_values:
    numerical_deriv = numerical_derivative(f, x0, h)
    error = abs(numerical_deriv - exact_deriv)
    errors.append(error)
    print(f"{h:<15.0e} {numerical_deriv:<20.15f} {error:<20.2e}")

print("\nObservations:")
print("• h too large (1e-1): Large truncation error")
print("• h moderate (1e-4): Minimum error")
print("• h too small (1e-16): Roundoff error dominates, result completely wrong!")

# Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Left plot: Error vs step size
ax1.loglog(h_values, errors, 'bo-', linewidth=2, markersize=8)
ax1.axhline(y=np.finfo(float).eps, color='r', linestyle='--', 
           linewidth=2, label='Machine epsilon (ε)')
ax1.set_xlabel('Step size h', fontsize=12, weight='bold')
ax1.set_ylabel('Absolute error', fontsize=12, weight='bold')
ax1.set_title('Numerical Differentiation Error vs Step Size\n(Log-log scale)', 
             fontsize=13, weight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=11)

# Mark optimal point
min_error_idx = np.argmin(errors)
ax1.plot(h_values[min_error_idx], errors[min_error_idx], 
        'r*', markersize=20, label='Optimal step size')
ax1.text(h_values[min_error_idx], errors[min_error_idx] * 3, 
        f'Optimal h ≈ {h_values[min_error_idx]:.0e}', 
        fontsize=10, weight='bold', ha='center')

# Right plot: Derivative approximations with different step sizes
x_range = np.linspace(0, 2*np.pi, 100)
ax2.plot(x_range, f_derivative_exact(x_range), 'b-', 
        linewidth=3, label='Exact derivative cos(x)')

for h in [1e-2, 1e-8, 1e-14]:
    numerical_derivs = [numerical_derivative(f, x, h) for x in x_range]
    ax2.plot(x_range, numerical_derivs, '--', linewidth=2, 
            label=f'Numerical derivative (h={h:.0e})', alpha=0.7)

ax2.axvline(x=x0, color='r', linestyle=':', alpha=0.5)
ax2.set_xlabel('x', fontsize=12, weight='bold')
ax2.set_ylabel("f'(x)", fontsize=12, weight='bold')
ax2.set_title('Numerical Differentiation Performance at Different Step Sizes', 
             fontsize=13, weight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=9)

plt.tight_layout()
plt.show()

# ========== Example 2: Computational Cost for High-Dimensional Functions ==========
print("\n" + "=" * 60)
print("Example 2: Computational Cost for High-Dimensional Functions")
print("=" * 60)

import time

def f_multidim(x):
    """High-dimensional function: f(x) = sum(x_i^2)"""
    return np.sum(x**2)

def numerical_gradient(f, x, h=1e-5):
    """Numerical gradient computation (requires 2n function evaluations)"""
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[i] += h
        x_minus[i] -= h
        grad[i] = (f(x_plus) - f(x_minus)) / (2 * h)
    return grad

def analytical_gradient(x):
    """Analytical gradient: ∇f = 2x"""
    return 2 * x

# Test different dimensions
dimensions = [10, 100, 1000, 5000]
print(f"\n{'Dimension':<10} {'Numerical gradient time':<25} {'Analytical gradient time':<25} {'Function calls':<15}")
print("-" * 80)

for n in dimensions:
    x = np.random.randn(n)
    
    # Numerical gradient
    start = time.time()
    num_grad = numerical_gradient(f_multidim, x)
    num_time = time.time() - start
    
    # Analytical gradient
    start = time.time()
    ana_grad = analytical_gradient(x)
    ana_time = time.time() - start
    
    # Verify correctness
    error = np.linalg.norm(num_grad - ana_grad)
    
    print(f"{n:<10} {num_time:<25.6f} {ana_time:<25.6f} {2*n:<15}")

print("\nObservations:")
print("• Numerical gradient requires 2n function evaluations (n is dimension)")
print("• Computation time grows linearly with dimension")
print("• Analytical gradient only needs 1 computation, much faster")
print("• For deep learning (millions of parameters), numerical gradient is completely infeasible!")

# Visualization of computational cost
fig, ax = plt.subplots(figsize=(10, 6))

# Re-test to get more data points
dims = [10, 50, 100, 200, 500, 1000, 2000]
num_times = []
ana_times = []

for n in dims:
    x = np.random.randn(n)
    
    start = time.time()
    _ = numerical_gradient(f_multidim, x)
    num_times.append(time.time() - start)
    
    start = time.time()
    _ = analytical_gradient(x)
    ana_times.append(time.time() - start)

ax.plot(dims, num_times, 'ro-', linewidth=3, markersize=8, 
       label='Numerical gradient (O(n))')
ax.plot(dims, ana_times, 'bo-', linewidth=3, markersize=8, 
       label='Analytical gradient (O(1))')

ax.set_xlabel('Dimension n', fontsize=13, weight='bold')
ax.set_ylabel('Computation time (seconds)', fontsize=13, weight='bold')
ax.set_title('Computational Cost: Numerical vs Analytical Gradient', 
            fontsize=14, weight='bold')
ax.grid(True, alpha=0.3)
ax.legend(fontsize=12)

# Add text annotation
ax.text(0.5, 0.8, 'Numerical gradient grows linearly with dimension\nAnalytical gradient remains nearly constant', 
       transform=ax.transAxes, fontsize=11, weight='bold',
       bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
       ha='center')

plt.tight_layout()
plt.show()
