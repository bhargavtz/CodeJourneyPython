# Python Libraries Cheat Sheet

## 1. **NumPy**
- **NumPy:** Fundamental library for numerical computing in Python.

```python
import numpy as np

# Creating Arrays
arr = np.array([1, 2, 3, 4])
matrix = np.array([[1, 2], [3, 4]])

# Basic Operations
print(arr + 1)            # Output: [2 3 4 5]
print(arr * 2)            # Output: [2 4 6 8]
print(matrix.T)           # Output: [[1 3]
                          #          [2 4]]

# Statistical Functions
mean = np.mean(arr)
std_dev = np.std(arr)

# Array Reshaping
reshaped = arr.reshape((2, 2))
```

## 2. **Pandas**
- **Pandas:** Data manipulation and analysis library.

```python
import pandas as pd

# Creating DataFrames
data = {'Name': ['Alice', 'Bob'], 'Age': [25, 30]}
df = pd.DataFrame(data)

# Accessing Data
print(df['Name'])         # Output: Series with Name column
print(df.iloc[0])         # Output: First row of the DataFrame

# Filtering Data
filtered_df = df[df['Age'] > 25]

# Adding New Column
df['City'] = ['NYC', 'LA']

# Handling Missing Data
df.dropna()               # Drop rows with missing values
df.fillna(0)              # Replace missing values with 0
```

## 3. **Matplotlib**
- **Matplotlib:** Plotting library for creating static, animated, and interactive visualizations.

```python
import matplotlib.pyplot as plt

# Basic Plot
plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
plt.title("Basic Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()

# Scatter Plot
plt.scatter([1, 2, 3, 4], [10, 20, 25, 30])
plt.title("Scatter Plot")
plt.show()

# Bar Plot
plt.bar(['A', 'B', 'C'], [10, 20, 15])
plt.title("Bar Plot")
plt.show()

# Histogram
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
plt.hist(data, bins=4)
plt.title("Histogram")
plt.show()
```

## 4. **Seaborn**
- **Seaborn:** Statistical data visualization library based on Matplotlib.

```python
import seaborn as sns
import pandas as pd

# Sample Data
data = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [10, 20, 25, 30],
    'category': ['A', 'B', 'A', 'B']
})

# Line Plot
sns.lineplot(x='x', y='y', data=data)
plt.show()

# Box Plot
sns.boxplot(x='category', y='y', data=data)
plt.show()

# Heatmap
sns.heatmap(data.corr(), annot=True)
plt.show()
```

## 5. **SciPy**
- **SciPy:** Library used for scientific and technical computing, built on NumPy.

```python
from scipy import stats
import numpy as np

# Statistical Functions
data = np.array([1, 2, 3, 4, 5, 6])
mean = np.mean(data)
median = np.median(data)
mode = stats.mode(data)

# Probability Distributions
norm_dist = stats.norm(loc=0, scale=1)  # Normal distribution
prob = norm_dist.cdf(1.96)              # Cumulative distribution function
```

## 6. **Scikit-Learn**
- **Scikit-Learn:** Machine learning library.

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Sample Data
X = [[1], [2], [3], [4]]
y = [10, 20, 25, 30]

# Splitting Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model Training
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, predictions)
```

## 7. **TensorFlow**
- **TensorFlow:** Open-source library for numerical computation and machine learning.

```python
import tensorflow as tf

# Creating Tensors
a = tf.constant(2)
b = tf.constant(3)

# Basic Operations
add = tf.add(a, b)
mult = tf.multiply(a, b)

# Simple Neural Network Example
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(units=1, input_shape=[1])
])
model.compile(optimizer='sgd', loss='mean_squared_error')
model.fit(X, y, epochs=500)
```

## 8. **Keras**
- **Keras:** High-level neural networks API, running on top of TensorFlow.


```python
import tensorflow as tf
from tensorflow.keras import layers, models

# Building a Simple Neural Network
model = models.Sequential([
    layers.Dense(64, activation='relu', input_shape=(100,)),
    layers.Dense(10, activation='softmax')
])

# Compiling the Model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Training the Model
model.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val))

# Evaluating the Model
loss, accuracy = model.evaluate(X_test, y_test)
```

## **zipfile**
- **zipfile:** Module for working with ZIP archives in Python.

```python
import zipfile

# Creating a ZIP file
with zipfile.ZipFile('example.zip', 'w') as zipf:
    zipf.write('file1.txt')
    zipf.write('file2.txt')

# Extracting a ZIP file
with zipfile.ZipFile('example.zip', 'r') as zipf:
    zipf.extractall('extracted_files')

# Listing contents of a ZIP file
with zipfile.ZipFile('example.zip', 'r') as zipf:
    print(zipf.namelist())  # Output: ['file1.txt', 'file2.txt']
```

## **Image Processing Libraries**

### **Pillow**
- **Pillow:** Python Imaging Library (PIL) fork, used for opening, manipulating, and saving images.

```python
from PIL import Image

# Opening an Image
image = Image.open('example.jpg')

# Resizing an Image
resized_image = image.resize((200, 300))

# Rotating an Image
rotated_image = image.rotate(45)

# Saving an Image
rotated_image.save('rotated_example.jpg')

# Converting to Grayscale
gray_image = image.convert('L')
gray_image.save('gray_example.jpg')
```

### **OpenCV**
- **OpenCV:** Library for real-time computer vision.

```python
import cv2

# Reading an Image
image = cv2.imread('example.jpg')

# Displaying an Image
cv2.imshow('Image', image)
cv2.waitKey(0)  # Waits for a key press to close the window
cv2.destroyAllWindows()

# Converting to Grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite('gray_example.jpg', gray_image)

# Resizing an Image
resized_image = cv2.resize(image, (200, 300))
cv2.imwrite('resized_example.jpg', resized_image)
```
