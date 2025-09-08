# Complete NumPy Tutorial: From Beginner to Advanced

## Table of Contents
1. [Introduction to NumPy](#introduction)
2. [Basic Array Creation and Manipulation](#basic-arrays)
3. [Array Operations and Mathematical Functions](#array-operations)
4. [Indexing and Slicing Techniques](#indexing-slicing)
5. [Broadcasting](#broadcasting)
6. [Linear Algebra Operations](#linear-algebra)
7. [Statistical Functions](#statistical-functions)
8. [Random Number Generation](#random-numbers)
9. [Advanced Array Manipulation](#advanced-manipulation)
10. [Performance Considerations and Best Practices](#performance-best-practices)

---

## 1. Introduction to NumPy {#introduction}

NumPy (Numerical Python) is the foundational library for scientific computing in Python. It provides:
- High-performance multidimensional arrays (ndarray)
- Mathematical functions operating on arrays
- Tools for integrating with C/C++ and Fortran code
- Linear algebra, Fourier transform, and random number capabilities

### Installation and Import
```python
# Install NumPy (if not already installed)
# pip install numpy

import numpy as np
print(f"NumPy version: {np.__version__}")
```

### Why NumPy?
- **Performance**: Operations are implemented in C, making them much faster than pure Python
- **Memory Efficiency**: Arrays use contiguous memory layout
- **Vectorization**: Perform operations on entire arrays without explicit loops
- **Broadcasting**: Intelligent handling of arrays with different shapes

---

## 2. Basic Array Creation and Manipulation {#basic-arrays}

### 2.1 Creating Arrays

#### From Python Lists
```python
# 1D array
arr_1d = np.array([1, 2, 3, 4, 5])
print("1D array:", arr_1d)
print("Shape:", arr_1d.shape)
print("Data type:", arr_1d.dtype)

# 2D array
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
print("\n2D array:\n", arr_2d)
print("Shape:", arr_2d.shape)
print("Dimensions:", arr_2d.ndim)

# 3D array
arr_3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
print("\n3D array:\n", arr_3d)
print("Shape:", arr_3d.shape)
```

#### Using Built-in Functions
```python
# Array of zeros
zeros_arr = np.zeros((3, 4))
print("Zeros array:\n", zeros_arr)

# Array of ones
ones_arr = np.ones((2, 3, 2))
print("\nOnes array shape:", ones_arr.shape)  

# Array filled with a specific value
full_arr = np.full((2, 3), 7)
print("\nFull array:\n", full_arr)

# Identity matrix
identity = np.eye(4)
print("\nIdentity matrix:\n", identity)

# Array with range of values
range_arr = np.arange(0, 10, 2)  # start, stop, step
print("\nRange array:", range_arr)

# Linearly spaced array
linspace_arr = np.linspace(0, 1, 5)  # start, stop, num_points
print("Linspace array:", linspace_arr)

# Logarithmically spaced array
logspace_arr = np.logspace(0, 2, 5)  # 10^0 to 10^2, 5 points
print("Logspace array:", logspace_arr)
```

### 2.2 Array Properties
```python
arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])

print("Array:\n", arr)
print("Shape:", arr.shape)          # Dimensions
print("Size:", arr.size)            # Total number of elements
print("Ndim:", arr.ndim)            # Number of dimensions
print("Dtype:", arr.dtype)          # Data type
print("Itemsize:", arr.itemsize)    # Size of each element in bytes
print("Nbytes:", arr.nbytes)        # Total bytes consumed
```

### 2.3 Data Types
```python
# Specify data type during creation
int_arr = np.array([1, 2, 3], dtype=np.int32)
float_arr = np.array([1, 2, 3], dtype=np.float64)
complex_arr = np.array([1+2j, 3+4j], dtype=np.complex128)

print("Integer array:", int_arr.dtype)
print("Float array:", float_arr.dtype)
print("Complex array:", complex_arr.dtype)

# Convert data types
arr = np.array([1.7, 2.3, 3.9])
int_converted = arr.astype(np.int32)
print("\nOriginal:", arr)
print("Converted to int:", int_converted)
```

### 2.4 Array Reshaping
```python
# Create a 1D array
arr_1d = np.arange(12)
print("Original 1D array:", arr_1d)

# Reshape to 2D
arr_2d = arr_1d.reshape(3, 4)
print("\nReshaped to 3x4:\n", arr_2d)

# Reshape to 3D
arr_3d = arr_1d.reshape(2, 2, 3)
print("\nReshaped to 2x2x3:\n", arr_3d)

# Automatic dimension calculation
auto_reshape = arr_1d.reshape(4, -1)  # -1 means "figure out this dimension"
print("\nAuto reshape (4, -1):\n", auto_reshape)

# Flatten array
flattened = arr_2d.flatten()
print("\nFlattened:", flattened)

# Ravel (returns view if possible)
raveled = arr_2d.ravel()
print("Raveled:", raveled)
```

---

## 3. Array Operations and Mathematical Functions {#array-operations}

### 3.1 Arithmetic Operations
```python
arr1 = np.array([1, 2, 3, 4])
arr2 = np.array([5, 6, 7, 8])

# Element-wise operations
print("Addition:", arr1 + arr2)
print("Subtraction:", arr1 - arr2)
print("Multiplication:", arr1 * arr2)
print("Division:", arr1 / arr2)
print("Power:", arr1 ** 2)
print("Modulo:", arr2 % 3)

# Scalar operations
print("\nScalar operations:")
print("Add 10:", arr1 + 10)
print("Multiply by 2:", arr1 * 2)
print("Divide by 2:", arr1 / 2)
```

### 3.2 Universal Functions (ufuncs)
```python
arr = np.array([0, np.pi/4, np.pi/2, np.pi])

# Trigonometric functions
print("Array:", arr)
print("Sine:", np.sin(arr))
print("Cosine:", np.cos(arr))
print("Tangent:", np.tan(arr))

# Exponential and logarithmic functions
arr_pos = np.array([1, 2, 3, 4])
print("\nExponential:", np.exp(arr_pos))
print("Natural log:", np.log(arr_pos))
print("Log base 10:", np.log10(arr_pos))
print("Square root:", np.sqrt(arr_pos))

# Rounding functions
arr_float = np.array([1.2, 2.7, 3.1, 4.8])
print("\nOriginal:", arr_float)
print("Round:", np.round(arr_float))
print("Floor:", np.floor(arr_float))
print("Ceiling:", np.ceil(arr_float))
```

### 3.3 Comparison Operations
```python
arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([1, 3, 2, 4, 6])

# Element-wise comparisons
print("Equal:", arr1 == arr2)
print("Not equal:", arr1 != arr2)
print("Less than:", arr1 < arr2)
print("Greater than:", arr1 > arr2)
print("Less or equal:", arr1 <= arr2)

# Logical operations
bool_arr1 = np.array([True, False, True, False])
bool_arr2 = np.array([True, True, False, False])

print("\nLogical AND:", np.logical_and(bool_arr1, bool_arr2))
print("Logical OR:", np.logical_or(bool_arr1, bool_arr2))
print("Logical NOT:", np.logical_not(bool_arr1))
```

### 3.4 Aggregate Functions
```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

print("Array:\n", arr)
print("Sum:", np.sum(arr))
print("Sum along axis 0:", np.sum(arr, axis=0))  # Column sums
print("Sum along axis 1:", np.sum(arr, axis=1))  # Row sums

print("\nMin:", np.min(arr))
print("Max:", np.max(arr))
print("Mean:", np.mean(arr))
print("Median:", np.median(arr))
print("Standard deviation:", np.std(arr))

# Cumulative operations
print("\nCumulative sum:", np.cumsum(arr))
print("Cumulative product:", np.cumprod(arr))
```

---

## 4. Indexing and Slicing Techniques {#indexing-slicing}

### 4.1 Basic Indexing
```python
# 1D array indexing
arr_1d = np.array([10, 20, 30, 40, 50])
print("1D array:", arr_1d)
print("First element:", arr_1d[0])
print("Last element:", arr_1d[-1])
print("Second to last:", arr_1d[-2])

# 2D array indexing
arr_2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("\n2D array:\n", arr_2d)
print("Element at (1,2):", arr_2d[1, 2])  # Row 1, Column 2
print("Element at (0,0):", arr_2d[0, 0])  # Row 0, Column 0
```

### 4.2 Slicing
```python
arr = np.arange(20).reshape(4, 5)
print("Original array:\n", arr)

# Basic slicing
print("\nFirst 2 rows:", arr[:2])
print("Last 2 columns:", arr[:, -2:])
print("Every other row:", arr[::2])
print("Reverse rows:", arr[::-1])

# Advanced slicing
print("\nRows 1-3, columns 1-4:")
print(arr[1:3, 1:4])

print("\nEvery other element in both dimensions:")
print(arr[::2, ::2])
```

### 4.3 Boolean Indexing
```python
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Create boolean mask
mask = arr > 5
print("Array:", arr)
print("Mask (arr > 5):", mask)
print("Elements > 5:", arr[mask])

# Direct boolean indexing
print("Even numbers:", arr[arr % 2 == 0])
print("Numbers between 3 and 7:", arr[(arr >= 3) & (arr <= 7)])

# 2D boolean indexing
arr_2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("\n2D array:\n", arr_2d)
print("Elements > 5:\n", arr_2d[arr_2d > 5])
```

### 4.4 Fancy Indexing
```python
arr = np.array([10, 20, 30, 40, 50, 60])

# Index with list of integers
indices = [0, 2, 4]
print("Array:", arr)
print("Elements at indices [0, 2, 4]:", arr[indices])

# 2D fancy indexing
arr_2d = np.arange(24).reshape(6, 4)
print("\n2D array:\n", arr_2d)

# Select specific rows
rows = [0, 2, 4]
print("Rows [0, 2, 4]:\n", arr_2d[rows])

# Select specific elements
rows = [0, 1, 2]
cols = [1, 2, 3]
print("Elements at (0,1), (1,2), (2,3):", arr_2d[rows, cols])
```

### 4.5 Advanced Indexing Techniques
```python
# Using where function
arr = np.array([1, 2, 3, 4, 5, 6])
result = np.where(arr > 3, arr, 0)  # Replace elements <= 3 with 0
print("Original:", arr)
print("Where > 3:", result)

# Multiple conditions with where
result2 = np.where((arr > 2) & (arr < 5), arr * 2, arr)
print("Conditional transformation:", result2)

# argmax and argmin
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])
print("\nArray:", arr)
print("Index of max element:", np.argmax(arr))
print("Index of min element:", np.argmin(arr))

# For 2D arrays
arr_2d = np.random.randint(0, 10, (3, 4))
print("\n2D array:\n", arr_2d)
print("Argmax (flattened):", np.argmax(arr_2d))
print("Argmax along axis 0:", np.argmax(arr_2d, axis=0))
print("Argmax along axis 1:", np.argmax(arr_2d, axis=1))
```

---

## 5. Broadcasting {#broadcasting}

### 5.1 Understanding Broadcasting
Broadcasting allows NumPy to perform operations on arrays with different shapes without explicitly reshaping them.

```python
# Basic broadcasting example
arr = np.array([[1, 2, 3], [4, 5, 6]])
scalar = 10

print("Array:\n", arr)
print("Scalar:", scalar)
print("Array + Scalar:\n", arr + scalar)

# Broadcasting with 1D array
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
arr_1d = np.array([10, 20, 30])

print("\n2D array:\n", arr_2d)
print("1D array:", arr_1d)
print("2D + 1D:\n", arr_2d + arr_1d)
```

### 5.2 Broadcasting Rules
```python
# Rule 1: Arrays are aligned from the rightmost dimension
arr1 = np.ones((3, 4))
arr2 = np.ones((4,))
result = arr1 + arr2  # Works: (3,4) + (4,) -> (3,4)
print("Shape result:", result.shape)

# Rule 2: Dimensions of size 1 are stretched
arr1 = np.ones((3, 1))
arr2 = np.ones((1, 4))
result = arr1 + arr2  # (3,1) + (1,4) -> (3,4)
print("Broadcasting (3,1) + (1,4):", result.shape)

# Rule 3: Missing dimensions are assumed to be 1
arr1 = np.ones((3, 4, 5))
arr2 = np.ones((5,))
result = arr1 + arr2  # (3,4,5) + (5,) -> (3,4,5)
print("Broadcasting (3,4,5) + (5,):", result.shape)
```

### 5.3 Practical Broadcasting Examples
```python
# Normalize rows of a matrix
data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)
row_means = np.mean(data, axis=1, keepdims=True)

print("Original data:\n", data)
print("Row means:\n", row_means)
print("Normalized data:\n", data - row_means)

# Distance matrix calculation
points = np.array([[1, 2], [3, 4], [5, 6]])
# Using broadcasting to calculate all pairwise distances
diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
distances = np.sqrt(np.sum(diff**2, axis=2))
print("\nPoints:\n", points)
print("Distance matrix:\n", distances)

# Image processing example simulation
image = np.random.randint(0, 256, (100, 100, 3))  # RGB image
mean_color = np.mean(image, axis=(0, 1))  # Mean color across spatial dimensions
normalized_image = image - mean_color  # Broadcasting across spatial dimensions
print(f"\nImage shape: {image.shape}")
print(f"Mean color: {mean_color}")
print(f"Normalized image shape: {normalized_image.shape}")
```

---

## 6. Linear Algebra Operations {#linear-algebra}

### 6.1 Basic Linear Algebra
```python
# Matrix creation
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print("Matrix A:\n", A)
print("Matrix B:\n", B)

# Matrix multiplication
C = np.dot(A, B)  # or A @ B (Python 3.5+)
print("\nA @ B:\n", C)

# Matrix transpose
print("\nA transpose:\n", A.T)

# Matrix determinant
det_A = np.linalg.det(A)
print("\nDeterminant of A:", det_A)

# Matrix inverse
A_inv = np.linalg.inv(A)
print("\nInverse of A:\n", A_inv)

# Verify inverse
identity = A @ A_inv
print("\nA @ A_inv (should be identity):\n", identity)
```

### 6.2 Eigenvalues and Eigenvectors
```python
# Create a symmetric matrix for real eigenvalues
matrix = np.array([[4, 2], [2, 3]])

# Calculate eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(matrix)

print("Matrix:\n", matrix)
print("\nEigenvalues:", eigenvalues)
print("Eigenvectors:\n", eigenvectors)

# Verify: A * v = λ * v
for i in range(len(eigenvalues)):
    left_side = matrix @ eigenvectors[:, i]
    right_side = eigenvalues[i] * eigenvectors[:, i]
    print(f"\nVerification for eigenvalue {eigenvalues[i]:.3f}:")
    print("A @ v =", left_side)
    print("λ * v =", right_side)
    print("Close?", np.allclose(left_side, right_side))
```

### 6.3 Solving Linear Systems
```python
# Solve Ax = b
A = np.array([[2, 1], [1, 3]])
b = np.array([5, 6])

print("Matrix A:\n", A)
print("Vector b:", b)

# Solve the system
x = np.linalg.solve(A, b)
print("\nSolution x:", x)

# Verify solution
verification = A @ x
print("Verification A @ x:", verification)
print("Should equal b:", b)
print("Close?", np.allclose(verification, b))

# Least squares solution for overdetermined systems
A_over = np.array([[1, 1], [2, 1], [3, 1]])  # 3 equations, 2 unknowns
b_over = np.array([2, 3, 4])

x_ls = np.linalg.lstsq(A_over, b_over, rcond=None)[0]
print(f"\nLeast squares solution: {x_ls}")
```

### 6.4 Matrix Decompositions
```python
# SVD (Singular Value Decomposition)
A = np.array([[1, 2, 3], [4, 5, 6]])
U, s, Vt = np.linalg.svd(A)

print("Original matrix A:\n", A)
print("\nU shape:", U.shape)
print("s (singular values):", s)
print("Vt shape:", Vt.shape)

# Reconstruct matrix
A_reconstructed = U @ np.diag(s) @ Vt
print("\nReconstructed A:\n", A_reconstructed)
print("Close to original?", np.allclose(A, A_reconstructed))

# QR decomposition
A_square = np.array([[1, 2], [3, 4]], dtype=float)
Q, R = np.linalg.qr(A_square)

print(f"\nOriginal matrix:\n{A_square}")
print(f"\nQ (orthogonal):\n{Q}")
print(f"\nR (upper triangular):\n{R}")
print(f"\nQ @ R:\n{Q @ R}")
print("Q is orthogonal?", np.allclose(Q @ Q.T, np.eye(2)))
```

### 6.5 Matrix Norms and Condition Numbers
```python
A = np.array([[1, 2], [3, 4]])

# Different types of norms
frobenius_norm = np.linalg.norm(A, 'fro')
l2_norm = np.linalg.norm(A, 2)
l1_norm = np.linalg.norm(A, 1)
inf_norm = np.linalg.norm(A, np.inf)

print("Matrix A:\n", A)
print(f"\nFrobenius norm: {frobenius_norm:.3f}")
print(f"L2 norm: {l2_norm:.3f}")
print(f"L1 norm: {l1_norm:.3f}")
print(f"Infinity norm: {inf_norm:.3f}")

# Condition number
cond_num = np.linalg.cond(A)
print(f"\nCondition number: {cond_num:.3f}")
```

---

## 7. Statistical Functions {#statistical-functions}

### 7.1 Descriptive Statistics
```python
# Generate sample data
np.random.seed(42)
data = np.random.normal(10, 2, 1000)  # Normal distribution, mean=10, std=2

print("Data shape:", data.shape)
print("First 10 values:", data[:10])

# Basic statistics
print(f"\nMean: {np.mean(data):.3f}")
print(f"Median: {np.median(data):.3f}")
print(f"Standard deviation: {np.std(data):.3f}")
print(f"Variance: {np.var(data):.3f}")
print(f"Min: {np.min(data):.3f}")
print(f"Max: {np.max(data):.3f}")

# Percentiles
percentiles = [25, 50, 75, 90, 95]
print(f"\nPercentiles {percentiles}:")
for p in percentiles:
    print(f"{p}th percentile: {np.percentile(data, p):.3f}")
```

### 7.2 Multi-dimensional Statistics
```python
# 2D data example
data_2d = np.random.rand(5, 4)
print("2D data:\n", data_2d)

# Statistics along different axes
print(f"\nMean along axis 0 (columns): {np.mean(data_2d, axis=0)}")
print(f"Mean along axis 1 (rows): {np.mean(data_2d, axis=1)}")
print(f"Overall mean: {np.mean(data_2d)}")

print(f"\nStd along axis 0: {np.std(data_2d, axis=0)}")
print(f"Std along axis 1: {np.std(data_2d, axis=1)}")

# Correlation and covariance
data_multi = np.random.multivariate_normal([0, 1, 2], [[1, 0.5, 0.2], 
                                                        [0.5, 1, 0.3], 
                                                        [0.2, 0.3, 1]], 100)
print(f"\nMultivariate data shape: {data_multi.shape}")

# Correlation matrix
corr_matrix = np.corrcoef(data_multi.T)
print("Correlation matrix:\n", corr_matrix)

# Covariance matrix
cov_matrix = np.cov(data_multi.T)
print("\nCovariance matrix:\n", cov_matrix)
```

### 7.3 Histograms and Binning
```python
# Generate data
data = np.random.exponential(2, 1000)

# Create histogram
counts, bin_edges = np.histogram(data, bins=20)
print("Histogram counts:", counts[:5], "...")
print("Bin edges:", bin_edges[:5], "...")

# 2D histogram
x = np.random.normal(0, 1, 1000)
y = x + np.random.normal(0, 0.5, 1000)  # Correlated data

hist_2d, x_edges, y_edges = np.histogram2d(x, y, bins=20)
print(f"\n2D histogram shape: {hist_2d.shape}")

# Digitize - bin data into discrete bins
data_sample = np.array([0.2, 1.5, 2.8, 4.1, 5.9])
bins = np.array([0, 1, 2, 3, 4, 5, 6])
bin_indices = np.digitize(data_sample, bins)
print(f"\nData: {data_sample}")
print(f"Bins: {bins}")
print(f"Bin indices: {bin_indices}")
```

### 7.4 Advanced Statistical Functions
```python
# Quantiles and percentile ranks
data = np.random.lognormal(0, 1, 1000)

# Quantiles
quantiles = np.quantile(data, [0.1, 0.25, 0.5, 0.75, 0.9])
print("Quantiles [10%, 25%, 50%, 75%, 90%]:", quantiles)

# Percentile rank
value = 2.0
rank = np.sum(data <= value) / len(data) * 100
print(f"\nPercentile rank of {value}: {rank:.1f}%")

# Weighted statistics
values = np.array([1, 2, 3, 4, 5])
weights = np.array([1, 1, 2, 1, 1])
weighted_mean = np.average(values, weights=weights)
print(f"\nValues: {values}")
print(f"Weights: {weights}")
print(f"Weighted mean: {weighted_mean:.3f}")
```

---

## 8. Random Number Generation {#random-numbers}

### 8.1 Basic Random Functions
```python
# Set seed for reproducibility
np.random.seed(42)

# Basic random numbers
print("Random float [0,1):", np.random.random())
print("Random floats:", np.random.random(5))

# Random integers
print("\nRandom int [0,10):", np.random.randint(0, 10))
print("Random ints:", np.random.randint(0, 10, 5))
print("Random ints 2D:", np.random.randint(0, 10, (2, 3)))

# Random choice
choices = ['apple', 'banana', 'cherry', 'date']
print(f"\nRandom choice: {np.random.choice(choices)}")
print(f"Random choices: {np.random.choice(choices, 3)}")
print(f"Random choices (no replacement): {np.random.choice(choices, 3, replace=False)}")

# Weighted random choice
weights = [0.1, 0.2, 0.3, 0.4]
print(f"Weighted choice: {np.random.choice(choices, 5, p=weights)}")
```

### 8.2 Probability Distributions
```python
# Normal distribution
normal_samples = np.random.normal(loc=0, scale=1, size=1000)
print("Normal distribution stats:")
print(f"Mean: {np.mean(normal_samples):.3f}")
print(f"Std: {np.std(normal_samples):.3f}")

# Uniform distribution
uniform_samples = np.random.uniform(low=0, high=10, size=1000)
print(f"\nUniform [0,10] mean: {np.mean(uniform_samples):.3f}")

# Exponential distribution
exp_samples = np.random.exponential(scale=2, size=1000)
print(f"Exponential (scale=2) mean: {np.mean(exp_samples):.3f}")

# Binomial distribution
binomial_samples = np.random.binomial(n=10, p=0.3, size=1000)
print(f"Binomial (n=10, p=0.3) mean: {np.mean(binomial_samples):.3f}")

# Poisson distribution
poisson_samples = np.random.poisson(lam=3, size=1000)
print(f"Poisson (λ=3) mean: {np.mean(poisson_samples):.3f}")

# Beta distribution
beta_samples = np.random.beta(a=2, b=5, size=1000)
print(f"Beta (a=2, b=5) mean: {np.mean(beta_samples):.3f}")
```

### 8.3 Multivariate Distributions
```python
# Multivariate normal
mean = [0, 1, 2]
cov = [[1, 0.5, 0.2], [0.5, 1, 0.3], [0.2, 0.3, 1]]
mvn_samples = np.random.multivariate_normal(mean, cov, 100)

print("Multivariate normal samples shape:", mvn_samples.shape)
print("Sample means:", np.mean(mvn_samples, axis=0))
print("Sample covariance:\n", np.cov(mvn_samples.T))

# Dirichlet distribution (useful for probability vectors)
alpha = [1, 2, 3]
dirichlet_samples = np.random.dirichlet(alpha, 5)
print(f"\nDirichlet samples (each row sums to 1):\n{dirichlet_samples}")
print("Row sums:", np.sum(dirichlet_samples, axis=1))
```

### 8.4 Random Sampling Techniques
```python
# Shuffling
arr = np.arange(10)
print("Original array:", arr)
np.random.shuffle(arr)  # In-place shuffle
print("Shuffled array:", arr)

# Random permutation (returns new array)
arr = np.arange(10)
permuted = np.random.permutation(arr)
print("Original:", arr)
print("Permuted:", permuted)

# Random sampling without replacement
population = np.arange(100)
sample = np.random.choice(population, size=10, replace=False)
print("Random sample of 10:", sample)

# Bootstrap sampling (with replacement)
data = np.array([1, 2, 3, 4, 5])
bootstrap_samples = np.random.choice(data, size=(1000, len(data)), replace=True)
bootstrap_means = np.mean(bootstrap_samples, axis=1)
print(f"Original data: {data}")
print(f"Bootstrap mean estimate: {np.mean(bootstrap_means):.3f}")
print(f"Bootstrap std of means: {np.std(bootstrap_means):.3f}")
```

### 8.5 Random State and Reproducibility
```python
# Using RandomState for more control
rng = np.random.RandomState(42)
print("Random numbers from rng:", rng.random(3))

# Multiple RandomState objects
rng1 = np.random.RandomState(42)
rng2 = np.random.RandomState(42)
print("rng1 samples:", rng1.random(3))
print("rng2 samples:", rng2.random(3))  # Same as rng1

# New random number generator (NumPy 1.17+)
from numpy.random import default_rng
rng_new = default_rng(42)
print("New RNG samples:", rng_new.random(3))

# Seeding for reproducible experiments
def reproducible_experiment():
    np.random.seed(123)
    data = np.random.normal(0, 1, 100)
    return np.mean(data)

result1 = reproducible_experiment()
result2 = reproducible_experiment()
print(f"Experiment results: {result1:.6f}, {result2:.6f}")
print(f"Identical? {result1 == result2}")
```

---

## 9. Advanced Array Manipulation {#advanced-manipulation}

### 9.1 Array Concatenation and Splitting
```python
# Concatenation
arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])

# Concatenate along different axes
concat_axis0 = np.concatenate([arr1, arr2], axis=0)  # Vertical
concat_axis1 = np.concatenate([arr1, arr2], axis=1)  # Horizontal

print("Array 1:\n", arr1)
print("Array 2:\n", arr2)
print("Concatenate axis=0:\n", concat_axis0)
print("Concatenate axis=1:\n", concat_axis1)

# Vertical and horizontal stack (convenience functions)
vstack_result = np.vstack([arr1, arr2])
hstack_result = np.hstack([arr1, arr2])
print("Vstack:\n", vstack_result)
print("Hstack:\n", hstack_result)

# Stack (creates new dimension)
stack_result = np.stack([arr1, arr2], axis=0)
print("Stack shape:", stack_result.shape)
print("Stack result:\n", stack_result)

# Splitting arrays
large_array = np.arange(12).reshape(4, 3)
print("\nLarge array:\n", large_array)

# Split into equal parts
split_arrays = np.split(large_array, 2, axis=0)  # Split into 2 parts along axis 0
print("Split arrays:")
for i, arr in enumerate(split_arrays):
    print(f"Part {i}:\n{arr}")

# Split at specific indices
split_at_indices = np.split(large_array, [1, 3], axis=0)  # Split at rows 1 and 3
print("Split at indices [1, 3]:")
for i, arr in enumerate(split_at_indices):
    print(f"Part {i}:\n{arr}")
```

### 9.2 Array Tiling and Repetition
```python
# Tile arrays
base_array = np.array([[1, 2], [3, 4]])
print("Base array:\n", base_array)

# Tile in different dimensions
tiled_2x3 = np.tile(base_array, (2, 3))
print("Tiled (2,3):\n", tiled_2x3)

# Repeat elements
arr = np.array([1, 2, 3])
repeated = np.repeat(arr, 3)  # Repeat each element 3 times
print("\nOriginal:", arr)
print("Repeated:", repeated)

# Repeat with different counts
repeated_diff = np.repeat(arr, [1, 2, 3])
print("Repeated [1,2,3] times:", repeated_diff)

# Repeat along axis
arr_2d = np.array([[1, 2], [3, 4]])
repeated_axis0 = np.repeat(arr_2d, 2, axis=0)
repeated_axis1 = np.repeat(arr_2d, 3, axis=1)
print("\nOriginal 2D:\n", arr_2d)
print("Repeated along axis 0:\n", repeated_axis0)
print("Repeated along axis 1:\n", repeated_axis1)
```

### 9.3 Array Manipulation Functions
```python
# Transpose and swapaxes
arr_3d = np.arange(24).reshape(2, 3, 4)
print("3D array shape:", arr_3d.shape)

# Transpose (reverse all axes)
transposed = np.transpose(arr_3d)
print("Transposed shape:", transposed.shape)

# Swap specific axes
swapped = np.swapaxes(arr_3d, 0, 2)  # Swap first and last axes
print("Swapped axes 0,2 shape:", swapped.shape)

# Moveaxis
moved = np.moveaxis(arr_3d, 0, -1)  # Move first axis to last
print("Moved axis shape:", moved.shape)

# Squeeze and expand dimensions
arr_squeeze = np.array([[[1], [2], [3]]])
print("\nOriginal shape:", arr_squeeze.shape)
squeezed = np.squeeze(arr_squeeze)
print("Squeezed shape:", squeezed.shape)
print("Squeezed array:", squeezed)

# Add dimensions
expanded = np.expand_dims(squeezed, axis=1)
print("Expanded shape:", expanded.shape)

# newaxis is alias for None
arr_1d = np.array([1, 2, 3])
row_vector = arr_1d[np.newaxis, :]  # Shape: (1, 3)
col_vector = arr_1d[:, np.newaxis]  # Shape: (3, 1)
print("1D array shape:", arr_1d.shape)
print("Row vector shape:", row_vector.shape)
print("Column vector shape:", col_vector.shape)
```

### 9.4 Unique Elements and Set Operations
```python
# Finding unique elements
arr = np.array([1, 2, 2, 3, 3, 3, 4, 4, 4, 4])
unique_vals = np.unique(arr)
print("Array:", arr)
print("Unique values:", unique_vals)

# Get indices and counts
unique_vals, indices, counts = np.unique(arr, return_index=True, return_counts=True)
print("Unique values:", unique_vals)
print("First occurrence indices:", indices)
print("Counts:", counts)

# Set operations
arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([3, 4, 5, 6, 7])

intersection = np.intersect1d(arr1, arr2)
union = np.union1d(arr1, arr2)
setdiff = np.setdiff1d(arr1, arr2)  # Elements in arr1 but not arr2
setxor = np.setxor1d(arr1, arr2)   # Elements in either arr1 or arr2, but not both

print(f"\nArray 1: {arr1}")
print(f"Array 2: {arr2}")
print(f"Intersection: {intersection}")
print(f"Union: {union}")
print(f"Set difference (1-2): {setdiff}")
print(f"Symmetric difference: {setxor}")

# Check membership
is_member = np.isin(arr1, arr2)
print(f"arr1 elements in arr2: {is_member}")
```

### 9.5 Sorting and Searching
```python
# Basic sorting
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])
sorted_arr = np.sort(arr)
print("Original:", arr)
print("Sorted:", sorted_arr)

# Get sorting indices
sort_indices = np.argsort(arr)
print("Sort indices:", sort_indices)
print("Verify:", arr[sort_indices])

# Sort 2D array
arr_2d = np.array([[3, 1, 4], [1, 5, 9], [2, 6, 5]])
print("\n2D array:\n", arr_2d)
sorted_axis0 = np.sort(arr_2d, axis=0)  # Sort each column
sorted_axis1 = np.sort(arr_2d, axis=1)  # Sort each row
print("Sorted axis 0:\n", sorted_axis0)
print("Sorted axis 1:\n", sorted_axis1)

# Partial sorting (finding k smallest/largest)
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])
k = 3
k_smallest = np.partition(arr, k)[:k+1]  # k+1 because partition puts kth element in correct position
print(f"\nOriginal: {arr}")
print(f"{k} smallest elements: {np.sort(k_smallest)}")

# Binary search (array must be sorted)
sorted_arr = np.array([1, 2, 3, 4, 5, 7, 8, 9])
search_vals = [3, 6, 7]
positions = np.searchsorted(sorted_arr, search_vals)
print(f"\nSorted array: {sorted_arr}")
print(f"Search values: {search_vals}")
print(f"Insert positions: {positions}")
```

### 9.6 Memory Layout and Views vs Copies
```python
# Understanding views vs copies
original = np.arange(12).reshape(3, 4)
print("Original array:\n", original)

# View (shares memory)
view = original[1:3, 1:3]
print("\nView:\n", view)
print("View shares memory?", np.shares_memory(original, view))

# Modifying view affects original
view[0, 0] = 999
print("After modifying view:\n", original)

# Copy (independent memory)
original = np.arange(12).reshape(3, 4)  # Reset
copy = original[1:3, 1:3].copy()
print("\nCopy shares memory?", np.shares_memory(original, copy))

copy[0, 0] = 888
print("Original after modifying copy:\n", original)
print("Copy:\n", copy)

# Memory layout
arr = np.arange(12).reshape(3, 4)
print(f"\nArray shape: {arr.shape}")
print(f"Array strides: {arr.strides}")
print(f"Is C-contiguous? {arr.flags['C_CONTIGUOUS']}")
print(f"Is F-contiguous? {arr.flags['F_CONTIGUOUS']}")

# Transpose changes strides
arr_T = arr.T
print(f"\nTransposed strides: {arr_T.strides}")
print(f"Transposed C-contiguous? {arr_T.flags['C_CONTIGUOUS']}")

# Force contiguous copy
arr_T_copy = np.ascontiguousarray(arr_T)
print(f"Contiguous copy C-contiguous? {arr_T_copy.flags['C_CONTIGUOUS']}")
```

---

## 10. Performance Considerations and Best Practices {#performance-best-practices}

### 10.1 Vectorization vs Loops
```python
import time

# Compare vectorized operations vs Python loops
size = 1000000
arr1 = np.random.random(size)
arr2 = np.random.random(size)

# Python loop approach (slow)
start_time = time.time()
result_loop = []
for i in range(size):
    result_loop.append(arr1[i] * arr2[i])
result_loop = np.array(result_loop)
loop_time = time.time() - start_time

# Vectorized approach (fast)
start_time = time.time()
result_vectorized = arr1 * arr2
vectorized_time = time.time() - start_time

print(f"Loop time: {loop_time:.4f} seconds")
print(f"Vectorized time: {vectorized_time:.4f} seconds")
print(f"Speedup: {loop_time/vectorized_time:.1f}x")
print(f"Results equal? {np.allclose(result_loop, result_vectorized)}")
```

### 10.2 Memory Efficiency
```python
# Memory-efficient operations
large_array = np.random.random((1000, 1000))

# Bad: Creates intermediate arrays
# result = (large_array + 1) * 2 - 0.5

# Better: Use in-place operations when possible
result = large_array.copy()
result += 1      # In-place addition
result *= 2      # In-place multiplication
result -= 0.5    # In-place subtraction

# Use appropriate data types
# Default is float64, but float32 might be sufficient
arr_64 = np.random.random(1000000)  # float64
arr_32 = np.random.random(1000000).astype(np.float32)  # float32

print(f"float64 memory: {arr_64.nbytes / 1024**2:.1f} MB")
print(f"float32 memory: {arr_32.nbytes / 1024**2:.1f} MB")
print(f"Memory savings: {(1 - arr_32.nbytes/arr_64.nbytes)*100:.1f}%")

# Integer types for appropriate data
counts = np.random.randint(0, 256, 1000000, dtype=np.uint8)  # 0-255 range
print(f"uint8 memory: {counts.nbytes / 1024**2:.1f} MB")
```

### 10.3 Common Performance Pitfalls
```python
# Pitfall 1: Growing arrays in loops (very slow)
def slow_array_building(n):
    arr = np.array([])
    for i in range(n):
        arr = np.append(arr, i)  # Creates new array each time!
    return arr

# Better: Pre-allocate
def fast_array_building(n):
    arr = np.zeros(n)
    for i in range(n):
        arr[i] = i
    return arr

# Best: Use vectorized operations
def best_array_building(n):
    return np.arange(n)

# Timing comparison (with smaller n for demonstration)
n = 10000
start = time.time()
slow_result = slow_array_building(n)
slow_time = time.time() - start

start = time.time()
fast_result = fast_array_building(n)
fast_time = time.time() - start

start = time.time()
best_result = best_array_building(n)
best_time = time.time() - start

print(f"Slow (append): {slow_time:.4f}s")
print(f"Fast (pre-allocate): {fast_time:.4f}s")
print(f"Best (vectorized): {best_time:.6f}s")

# Pitfall 2: Unnecessary copies
arr = np.random.random((1000, 1000))

# Creates unnecessary copy
def bad_function(arr):
    arr_copy = arr.copy()  # Unnecessary if we're not modifying
    return np.sum(arr_copy)

# Works with original array
def good_function(arr):
    return np.sum(arr)  # No copy needed

print(f"Both functions give same result: {bad_function(arr) == good_function(arr)}")
```

### 10.4 Best Practices Summary
```python
# 1. Use appropriate data types
int_data = np.array([1, 2, 3, 4], dtype=np.int32)  # Not float64
bool_data = np.array([True, False, True], dtype=bool)  # Not int

# 2. Avoid unnecessary reshaping
arr = np.arange(1000000)
# Bad: repeated reshaping
for _ in range(100):
    temp = arr.reshape(-1, 1000).reshape(-1)

# Good: reshape once if needed
arr_reshaped = arr.reshape(-1, 1000)

# 3. Use views when possible
large_arr = np.random.random((10000, 10000))
subset = large_arr[1000:2000, 1000:2000]  # This is a view, not a copy

# 4. Leverage broadcasting
# Instead of explicit loops or tiling
matrix = np.random.random((1000, 500))
vector = np.random.random(500)
result = matrix + vector  # Broadcasting handles the rest

# 5. Use axis parameter for operations
data = np.random.random((1000, 100))
row_means = np.mean(data, axis=1)  # Much faster than looping
col_means = np.mean(data, axis=0)

print("Best practices implemented successfully!")
```

### 10.5 Profiling and Optimization
```python
# Simple timing function
def time_function(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return result, end - start

# Example: Different ways to compute pairwise distances
def distance_loops(points):
    """Slow: nested loops"""
    n = len(points)
    distances = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distances[i, j] = np.sqrt(np.sum((points[i] - points[j])**2))
    return distances

def distance_broadcasting(points):
    """Fast: broadcasting"""
    diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
    return np.sqrt(np.sum(diff**2, axis=2))

def distance_cdist(points):
    """Using scipy.spatial.distance.cdist would be even better"""
    # This is just for demonstration - requires scipy
    # from scipy.spatial.distance import cdist
    # return cdist(points, points)
    pass

# Test with small dataset
points = np.random.random((50, 3))

result1, time1 = time_function(distance_loops, points)
result2, time2 = time_function(distance_broadcasting, points)

print(f"Nested loops: {time1:.4f}s")
print(f"Broadcasting: {time2:.4f}s")
print(f"Speedup: {time1/time2:.1f}x")
print(f"Results match: {np.allclose(result1, result2)}")
```

---

## Conclusion

This comprehensive NumPy tutorial covers all essential aspects from basic array creation to advanced manipulation techniques. Key takeaways:

1. **Start with the basics**: Understanding array creation, data types, and basic operations
2. **Master indexing and slicing**: These are fundamental for data manipulation
3. **Leverage broadcasting**: Avoid explicit loops and let NumPy handle array operations efficiently
4. **Use vectorized operations**: Always prefer NumPy functions over Python loops
5. **Understand memory**: Know when operations create views vs copies
6. **Choose appropriate data types**: This can significantly impact memory usage
7. **Profile your code**: Measure performance to identify bottlenecks

### Next Steps
- Practice with real datasets
- Explore integration with pandas, matplotlib, and scikit-learn
- Learn about specialized NumPy functions for your domain (signal processing, image processing, etc.)
- Consider learning about parallel computing with libraries like Numba or Dask for even better performance

Remember: NumPy is the foundation of the entire Python scientific computing ecosystem. Mastering it will make you much more effective with other libraries like pandas, scikit-learn, TensorFlow, and PyTorch.