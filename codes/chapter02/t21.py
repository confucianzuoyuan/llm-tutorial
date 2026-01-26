import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import time

# ========== Example 1: Expression Swell Problem ==========
print("=" * 60)
print("Example 1: Expression Swell in Symbolic Differentiation")
print("=" * 60)

# Define symbolic variable
x = sp.Symbol('x')

# Simple function
f1 = sp.sin(x) * sp.cos(x)
print("\nOriginal function:")
print(f"f(x) = {f1}")
print(f"Length: {len(str(f1))} characters")

# First derivative
f1_prime = sp.diff(f1, x)
print("\nFirst derivative:")
print(f"f'(x) = {f1_prime}")
print(f"Length: {len(str(f1_prime))} characters")

# Second derivative
f1_double_prime = sp.diff(f1_prime, x)
print("\nSecond derivative:")
print(f"f''(x) = {f1_double_prime}")
print(f"Length: {len(str(f1_double_prime))} characters")

# Third derivative
f1_triple_prime = sp.diff(f1_double_prime, x)
print("\nThird derivative:")
print(f"f'''(x) = {f1_triple_prime}")
print(f"Length: {len(str(f1_triple_prime))} characters")

print("\n" + "-" * 60)
print("More complex example: Derivative of a product")
print("-" * 60)

# Complex function
f2 = (x**2 + 1) * (x**3 + 2*x) * (x**4 + 3)
print(f"\nOriginal function:")
print(f"f(x) = {f2}")
print(f"Expanded: {sp.expand(f2)}")
print(f"Length: {len(str(f2))} characters")

# Differentiate
f2_prime = sp.diff(f2, x)
print(f"\nFirst derivative (unsimplified):")
print(f"f'(x) = {f2_prime}")
print(f"Length: {len(str(f2_prime))} characters")

# Expand
f2_prime_expanded = sp.expand(f2_prime)
print(f"\nFirst derivative (expanded):")
print(f"f'(x) = {f2_prime_expanded}")
print(f"Length: {len(str(f2_prime_expanded))} characters")

# Simplify
f2_prime_simplified = sp.simplify(f2_prime)
print(f"\nFirst derivative (simplified):")
print(f"f'(x) = {f2_prime_simplified}")
print(f"Length: {len(str(f2_prime_simplified))} characters")

print("\nObservations:")
print("• Expression length grows exponentially with derivative order")
print("• Even after simplification, expressions remain complex")
print("• Contains many repeated subexpressions")

# Visualization of expression growth
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Left plot: Expression length growth
orders = [0, 1, 2, 3, 4]
f_test = sp.sin(x) * sp.cos(x) * sp.exp(x)
lengths = []
current_f = f_test

for order in orders:
    lengths.append(len(str(current_f)))
    if order < max(orders):
        current_f = sp.diff(current_f, x)

ax1.plot(orders, lengths, 'ro-', linewidth=3, markersize=10)
ax1.set_xlabel('Derivative order', fontsize=13, weight='bold')
ax1.set_ylabel('Expression length (characters)', fontsize=13, weight='bold')
ax1.set_title('Expression Swell in Symbolic Differentiation\nf(x) = sin(x)·cos(x)·exp(x)', 
             fontsize=13, weight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_xticks(orders)

# Add exponential growth curve fit
z = np.polyfit(orders, np.log(lengths), 1)
p = np.poly1d(z)
ax1.plot(orders, np.exp(p(orders)), 'b--', linewidth=2, 
        alpha=0.7, label='Exponential fit')
ax1.legend(fontsize=11)

# Right plot: Expression growth for different functions
test_functions = [
    (sp.sin(x), 'sin(x)'),
    (sp.sin(x) * sp.cos(x), 'sin(x)·cos(x)'),
    ((x**2 + 1) * (x + 1), '(x²+1)(x+1)'),
    (sp.exp(sp.sin(x)), 'exp(sin(x))')
]

for func, label in test_functions:
    lengths = []
    current = func
    for i in range(5):
        lengths.append(len(str(current)))
        current = sp.diff(current, x)
    ax2.plot(range(5), lengths, 'o-', linewidth=2, markersize=8, label=label)

ax2.set_xlabel('Derivative order', fontsize=13, weight='bold')
ax2.set_ylabel('Expression length (characters)', fontsize=13, weight='bold')
ax2.set_title('Expression Swell Comparison for Different Functions', 
             fontsize=13, weight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=10)
ax2.set_yscale('log')

plt.tight_layout()
plt.show()

# ========== Example 2: Computational Efficiency Problem ==========
print("\n" + "=" * 60)
print("Example 2: Computational Efficiency in Symbolic Differentiation")
print("=" * 60)

# Define a complex function
x = sp.Symbol('x')
f_complex = sp.sin(x) * sp.cos(x) * sp.exp(x) * sp.log(x + 1)

print("\nOriginal function:")
print(f"f(x) = {f_complex}")

# Differentiate
f_derivative = sp.diff(f_complex, x)
print("\nDerivative (symbolic form):")
print(f"f'(x) = {f_derivative}")

# Convert to numerical functions
f_numeric = sp.lambdify(x, f_complex, 'numpy')
f_derivative_numeric = sp.lambdify(x, f_derivative, 'numpy')

# Manually optimized version (with common subexpression elimination)
def f_manual(x_val):
    """Manually optimized function with shared subexpressions"""
    sin_x = np.sin(x_val)
    cos_x = np.cos(x_val)
    exp_x = np.exp(x_val)
    log_term = np.log(x_val + 1)
    return sin_x * cos_x * exp_x * log_term

def f_derivative_manual(x_val):
    """Manually optimized derivative with shared subexpressions"""
    sin_x = np.sin(x_val)
    cos_x = np.cos(x_val)
    exp_x = np.exp(x_val)
    log_term = np.log(x_val + 1)
    
    # Manually compute derivative, reusing subexpressions
    term1 = cos_x * cos_x * exp_x * log_term
    term2 = -sin_x * sin_x * exp_x * log_term
    term3 = sin_x * cos_x * exp_x * log_term
    term4 = sin_x * cos_x * exp_x / (x_val + 1)
    
    return term1 + term2 + term3 + term4

# Performance test
x_test = np.linspace(0.1, 10, 10000)
n_iterations = 100

print("\nPerformance comparison (10000 points, 100 iterations):")
print("-" * 60)

# Symbolic differentiation generated function
start = time.time()
for _ in range(n_iterations):
    result_symbolic = f_derivative_numeric(x_test)
time_symbolic = time.time() - start

# Manually optimized function
start = time.time()
for _ in range(n_iterations):
    result_manual = f_derivative_manual(x_test)
time_manual = time.time() - start

print(f"Symbolic differentiation generated function: {time_symbolic:.4f} seconds")
print(f"Manually optimized function:                {time_manual:.4f} seconds")
print(f"Speedup: {time_symbolic / time_manual:.2f}x")

# Verify result consistency
max_diff = np.max(np.abs(result_symbolic - result_manual))
print(f"\nResult difference (max absolute error): {max_diff:.2e}")

print("\nObservations:")
print("• Symbolic differentiation generated code doesn't optimize subexpressions")
print("• Manual optimization can significantly improve performance")
print("• Symbolic differentiation doesn't automatically perform CSE (Common Subexpression Elimination)")

# Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Left plot: Performance comparison
methods = ['Symbolic Diff\n(Unoptimized)', 'Manual Impl\n(Optimized)']
times = [time_symbolic, time_manual]
colors = ['red', 'green']

bars = ax1.bar(methods, times, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
ax1.set_ylabel('Computation time (seconds)', fontsize=13, weight='bold')
ax1.set_title('Symbolic Differentiation vs Manual Optimization\nComputational Efficiency Comparison', 
             fontsize=13, weight='bold')
ax1.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar, time_val in zip(bars, times):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{time_val:.4f}s',
            ha='center', va='bottom', fontsize=12, weight='bold')

# Right plot: Result verification
x_plot = np.linspace(0.1, 5, 100)
y_symbolic = f_derivative_numeric(x_plot)
y_manual = f_derivative_manual(x_plot)

ax2.plot(x_plot, y_symbolic, 'r-', linewidth=3, label='Symbolic diff', alpha=0.7)
ax2.plot(x_plot, y_manual, 'g--', linewidth=2, label='Manual optimization', alpha=0.7)
ax2.set_xlabel('x', fontsize=13, weight='bold')
ax2.set_ylabel("f'(x)", fontsize=13, weight='bold')
ax2.set_title('Result Verification (Both methods agree)', fontsize=13, weight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=12)

plt.tight_layout()
plt.show()

# Using SymPy's CSE (Common Subexpression Elimination)
print("\n" + "-" * 60)
print("Using SymPy's Common Subexpression Elimination (CSE)")
print("-" * 60)

# Apply CSE
replacements, reduced_exprs = sp.cse(f_derivative)

print("\nCommon subexpressions:")
for i, (var, expr) in enumerate(replacements):
    print(f"{var} = {expr}")

print("\nReduced expression:")
print(f"f'(x) = {reduced_exprs[0]}")

print("\nObservations:")
print("• CSE can identify and extract common subexpressions")
print("• But it needs to be called manually, not automatic")
print("• For complex expressions, CSE can significantly reduce computation")
