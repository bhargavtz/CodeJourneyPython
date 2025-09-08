# Comprehensive Pandas Deep-Dive Tutorial

## Table of Contents
1. [Introduction to Pandas](#introduction-to-pandas)
2. [Core Data Structures](#core-data-structures)
3. [Data Loading and Input/Output](#data-loading-and-inputoutput)
4. [Data Selection and Filtering](#data-selection-and-filtering)
5. [Data Cleaning and Missing Values](#data-cleaning-and-missing-values)
6. [Data Transformation and Manipulation](#data-transformation-and-manipulation)
7. [Grouping and Aggregation](#grouping-and-aggregation)
8. [Merging and Joining](#merging-and-joining)
9. [Reshaping and Pivoting](#reshaping-and-pivoting)
10. [Time Series Analysis](#time-series-analysis)
11. [Statistical Operations](#statistical-operations)
12. [Performance Optimization](#performance-optimization)
13. [Best Practices and Common Pitfalls](#best-practices-and-common-pitfalls)

---

## 1. Introduction to Pandas

### What is Pandas?

Pandas (Panel Data) is a powerful, open-source data manipulation and analysis library for Python. Created by Wes McKinney in 2008, it has become the cornerstone of data science in Python, providing high-performance, easy-to-use data structures and data analysis tools.

### Key Features and Advantages

- **Flexible data structures**: Series (1D) and DataFrame (2D)
- **Data alignment and missing data handling**
- **Size mutability**: columns can be inserted and deleted
- **Powerful group by functionality**
- **Tools for reading/writing data** between in-memory data structures and different formats
- **Intelligent label-based slicing and indexing**
- **Time series functionality**

### Installation and Import

```python
# Installation (run in terminal/command prompt)
# pip install pandas

# Standard import convention
import pandas as pd
import numpy as np

# Check version
print(f"Pandas version: {pd.__version__}")
```

---

## 2. Core Data Structures

### 2.1 Series - One-Dimensional Data

A Series is a one-dimensional labeled array capable of holding data of any type.

```python
# Creating Series from different data types

# From a list
series_from_list = pd.Series([1, 2, 3, 4, 5])
print("Series from list:")
print(series_from_list)
print()

# From a list with custom index
series_custom_index = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
print("Series with custom index:")
print(series_custom_index)
print()

# From a dictionary
data_dict = {'apple': 5, 'banana': 3, 'orange': 8}
series_from_dict = pd.Series(data_dict)
print("Series from dictionary:")
print(series_from_dict)
print()

# From numpy array
import numpy as np
series_from_numpy = pd.Series(np.random.randn(5), index=['A', 'B', 'C', 'D', 'E'])
print("Series from numpy array:")
print(series_from_numpy)
print()

# Series with different data types
mixed_series = pd.Series(['text', 42, 3.14, True])
print("Mixed data types Series:")
print(mixed_series)
print(f"Data types: {mixed_series.dtype}")
```

#### Series Attributes and Methods

```python
# Key Series attributes
sample_series = pd.Series([10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])

print(f"Values: {sample_series.values}")
print(f"Index: {sample_series.index}")
print(f"Data type: {sample_series.dtype}")
print(f"Shape: {sample_series.shape}")
print(f"Size: {sample_series.size}")
print(f"Name: {sample_series.name}")

# Setting a name
sample_series.name = "Sample Data"
print(f"Series name after setting: {sample_series.name}")
```

### 2.2 DataFrame - Two-Dimensional Data

A DataFrame is a 2-dimensional labeled data structure with columns of potentially different types.

```python
# Creating DataFrames from different sources

# From dictionary of lists
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'Age': [25, 30, 35, 28],
    'City': ['New York', 'London', 'Tokyo', 'Paris'],
    'Salary': [50000, 60000, 70000, 55000]
}
df_from_dict = pd.DataFrame(data)
print("DataFrame from dictionary:")
print(df_from_dict)
print()

# From list of dictionaries
data_list = [
    {'Name': 'Alice', 'Age': 25, 'City': 'New York'},
    {'Name': 'Bob', 'Age': 30, 'City': 'London'},
    {'Name': 'Charlie', 'Age': 35, 'City': 'Tokyo'}
]
df_from_list_dict = pd.DataFrame(data_list)
print("DataFrame from list of dictionaries:")
print(df_from_list_dict)
print()

# From numpy array with custom index and columns
np_data = np.random.randn(4, 3)
df_from_numpy = pd.DataFrame(
    np_data,
    index=['Row1', 'Row2', 'Row3', 'Row4'],
    columns=['Col1', 'Col2', 'Col3']
)
print("DataFrame from numpy array:")
print(df_from_numpy)
print()

# From Series
series1 = pd.Series([1, 2, 3], name='A')
series2 = pd.Series([4, 5, 6], name='B')
df_from_series = pd.DataFrame([series1, series2]).T  # Transpose
print("DataFrame from Series:")
print(df_from_series)
```

#### DataFrame Attributes and Methods

```python
# Key DataFrame attributes and methods
sample_df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [5, 6, 7, 8],
    'C': ['x', 'y', 'z', 'w']
})

print("DataFrame shape:", sample_df.shape)
print("DataFrame size:", sample_df.size)
print("DataFrame columns:", sample_df.columns.tolist())
print("DataFrame index:", sample_df.index.tolist())
print("DataFrame data types:")
print(sample_df.dtypes)
print()

# Info method - comprehensive overview
print("DataFrame info:")
sample_df.info()
print()

# Describe method - statistical summary
numeric_df = pd.DataFrame({
    'A': np.random.randn(100),
    'B': np.random.randn(100) * 2 + 5,
    'C': np.random.randint(1, 10, 100)
})
print("Statistical summary:")
print(numeric_df.describe())
```

---

## 3. Data Loading and Input/Output

### 3.1 Reading Data from Various Sources

```python
# CSV Files
# df = pd.read_csv('data.csv')
# df = pd.read_csv('data.csv', index_col=0)  # Use first column as index
# df = pd.read_csv('data.csv', usecols=['Col1', 'Col2'])  # Select specific columns

# Example with sample data
import io
csv_data = """Name,Age,City,Salary
Alice,25,New York,50000
Bob,30,London,60000
Charlie,35,Tokyo,70000
Diana,28,Paris,55000"""

df_csv = pd.read_csv(io.StringIO(csv_data))
print("DataFrame from CSV:")
print(df_csv)
print()

# Excel Files
# df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
# df = pd.read_excel('data.xlsx', sheet_name=0)  # First sheet

# JSON Files
json_data = '''[
    {"Name": "Alice", "Age": 25, "City": "New York", "Salary": 50000},
    {"Name": "Bob", "Age": 30, "City": "London", "Salary": 60000},
    {"Name": "Charlie", "Age": 35, "City": "Tokyo", "Salary": 70000}
]'''

df_json = pd.read_json(json_data)
print("DataFrame from JSON:")
print(df_json)
print()

# SQL Database (example syntax)
# import sqlite3
# conn = sqlite3.connect('database.db')
# df = pd.read_sql_query("SELECT * FROM table_name", conn)

# URL (web data)
# df = pd.read_csv('https://example.com/data.csv')
```

### 3.2 Writing Data to Various Formats

```python
# Sample DataFrame for export examples
export_df = pd.DataFrame({
    'Product': ['A', 'B', 'C', 'D'],
    'Sales': [100, 150, 200, 120],
    'Price': [10.5, 15.0, 20.0, 12.5]
})

# Export to CSV
# export_df.to_csv('output.csv', index=False)  # Without row indices
# export_df.to_csv('output.csv', index=True)   # With row indices

# Export to Excel
# export_df.to_excel('output.xlsx', sheet_name='Sales_Data', index=False)

# Export to JSON
json_output = export_df.to_json(orient='records', indent=2)
print("JSON export (records format):")
print(json_output)
print()

# Different JSON orientations
print("JSON orientations:")
print("Index:", export_df.to_json(orient='index'))
print("Values:", export_df.to_json(orient='values'))
print("Columns:", export_df.to_json(orient='columns'))
```

### 3.3 Advanced Reading Options

```python
# Reading with advanced options

# Custom separators and missing value handling
advanced_csv = """Name|Age|City|Salary
Alice|25|New York|50000
Bob||London|60000
Charlie|35||70000
Diana|28|Paris|N/A"""

df_advanced = pd.read_csv(
    io.StringIO(advanced_csv),
    sep='|',                    # Custom separator
    na_values=['N/A', ''],      # Custom missing value indicators
    dtype={'Age': 'float64'},   # Specify data types
    parse_dates=False           # Date parsing
)
print("Advanced CSV reading:")
print(df_advanced)
print("\nData types:")
print(df_advanced.dtypes)
```

---

## 4. Data Selection and Filtering

### 4.1 Column Selection

```python
# Sample DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'Age': [25, 30, 35, 28, 32],
    'City': ['New York', 'London', 'Tokyo', 'Paris', 'Berlin'],
    'Salary': [50000, 60000, 70000, 55000, 65000],
    'Department': ['IT', 'HR', 'IT', 'Finance', 'IT']
})

# Single column selection
name_column = df['Name']
print("Single column (returns Series):")
print(type(name_column))
print(name_column.head())
print()

# Multiple column selection
selected_columns = df[['Name', 'Age', 'Salary']]
print("Multiple columns (returns DataFrame):")
print(type(selected_columns))
print(selected_columns)
print()

# Column selection with dot notation (when column name is valid Python identifier)
ages = df.Age
print("Dot notation access:")
print(ages.head())
```

### 4.2 Row Selection and Indexing

```python
# Label-based selection with .loc
print("Label-based selection with .loc:")
print(df.loc[0])  # Single row by index
print()
print(df.loc[0:2])  # Multiple rows by index range (inclusive)
print()
print(df.loc[0:2, 'Name':'City'])  # Rows and columns by label
print()

# Position-based selection with .iloc
print("Position-based selection with .iloc:")
print(df.iloc[0])  # Single row by position
print()
print(df.iloc[0:3])  # Multiple rows by position range (exclusive)
print()
print(df.iloc[0:3, 1:4])  # Rows and columns by position
print()

# Boolean selection with .loc
print("Boolean selection:")
it_employees = df.loc[df['Department'] == 'IT']
print(it_employees)
```

### 4.3 Boolean Filtering

```python
# Basic boolean filtering
high_salary = df[df['Salary'] > 60000]
print("Employees with salary > 60000:")
print(high_salary)
print()

# Multiple conditions with & (and) and | (or)
young_high_earners = df[(df['Age'] < 30) & (df['Salary'] > 55000)]
print("Young high earners (Age < 30 AND Salary > 55000):")
print(young_high_earners)
print()

it_or_finance = df[(df['Department'] == 'IT') | (df['Department'] == 'Finance')]
print("IT or Finance employees:")
print(it_or_finance)
print()

# Using isin() for multiple value filtering
specific_cities = df[df['City'].isin(['New York', 'London', 'Tokyo'])]
print("Employees in specific cities:")
print(specific_cities)
print()

# String filtering
names_with_a = df[df['Name'].str.contains('a', case=False)]
print("Names containing 'a' (case insensitive):")
print(names_with_a)
```

### 4.4 Advanced Selection Techniques

```python
# Query method for complex filtering
query_result = df.query('Age > 30 and Salary < 70000')
print("Query method result:")
print(query_result)
print()

# Using where() method
df_where = df.where(df['Age'] > 30)
print("Where method (NaN for False conditions):")
print(df_where)
print()

# Sample method for random selection
sample_rows = df.sample(n=3, random_state=42)
print("Random sample of 3 rows:")
print(sample_rows)
print()

# nlargest and nsmallest
top_salaries = df.nlargest(3, 'Salary')
print("Top 3 salaries:")
print(top_salaries)
print()

bottom_ages = df.nsmallest(2, 'Age')
print("Bottom 2 ages:")
print(bottom_ages)
```

---

## 5. Data Cleaning and Missing Values

### 5.1 Identifying Missing Values

```python
# Create DataFrame with missing values
data_with_missing = {
    'A': [1, 2, np.nan, 4, 5],
    'B': [5, np.nan, np.nan, 8, 9],
    'C': [10, 11, 12, np.nan, 14],
    'D': ['x', 'y', None, 'w', 'z']
}
df_missing = pd.DataFrame(data_with_missing)

print("DataFrame with missing values:")
print(df_missing)
print()

# Check for missing values
print("Missing values check:")
print("isnull():")
print(df_missing.isnull())
print()

print("Sum of missing values per column:")
print(df_missing.isnull().sum())
print()

print("Any missing values per column:")
print(df_missing.isnull().any())
print()

print("Total missing values in DataFrame:")
print(df_missing.isnull().sum().sum())
```

### 5.2 Handling Missing Values

```python
# Dropping missing values
print("Original shape:", df_missing.shape)

# Drop rows with any missing values
df_dropna_rows = df_missing.dropna()
print("After dropping rows with any NaN:", df_dropna_rows.shape)
print(df_dropna_rows)
print()

# Drop columns with any missing values
df_dropna_cols = df_missing.dropna(axis=1)
print("After dropping columns with any NaN:", df_dropna_cols.shape)
print(df_dropna_cols)
print()

# Drop rows with missing values in specific columns
df_dropna_specific = df_missing.dropna(subset=['A', 'B'])
print("After dropping rows with NaN in columns A or B:")
print(df_dropna_specific)
print()

# Require minimum number of non-null values
df_dropna_thresh = df_missing.dropna(thresh=3)  # At least 3 non-null values
print("Rows with at least 3 non-null values:")
print(df_dropna_thresh)
```

### 5.3 Filling Missing Values

```python
# Fill with constant values
df_filled_constant = df_missing.fillna(0)
print("Filled with constant (0):")
print(df_filled_constant)
print()

# Fill with different values for different columns
fill_values = {'A': 0, 'B': -1, 'C': 999, 'D': 'missing'}
df_filled_dict = df_missing.fillna(fill_values)
print("Filled with dictionary values:")
print(df_filled_dict)
print()

# Forward fill and backward fill
df_ffill = df_missing.fillna(method='ffill')  # Forward fill
print("Forward fill:")
print(df_ffill)
print()

df_bfill = df_missing.fillna(method='bfill')  # Backward fill
print("Backward fill:")
print(df_bfill)
print()

# Fill with statistical measures
df_filled_mean = df_missing.fillna(df_missing.mean())
print("Filled with column means:")
print(df_filled_mean)
print()

# Interpolation for numerical data
df_interpolated = df_missing.interpolate()
print("Interpolated values:")
print(df_interpolated)
```

### 5.4 Advanced Missing Value Handling

```python
# Create time series data with missing values
dates = pd.date_range('2024-01-01', periods=10, freq='D')
ts_data = pd.Series([1, 2, np.nan, 4, np.nan, 6, 7, np.nan, 9, 10], index=dates)

print("Time series with missing values:")
print(ts_data)
print()

# Time-based interpolation
ts_interpolated = ts_data.interpolate(method='time')
print("Time-based interpolation:")
print(ts_interpolated)
print()

# Replace specific values
df_replace = df_missing.replace({np.nan: -999, None: 'NULL'})
print("Replace with specific values:")
print(df_replace)
print()

# Using transform for group-wise filling
grouped_data = pd.DataFrame({
    'Group': ['A', 'A', 'B', 'B', 'A', 'B'],
    'Value': [1, np.nan, 3, 4, np.nan, 6]
})

grouped_filled = grouped_data.copy()
grouped_filled['Value'] = grouped_data.groupby('Group')['Value'].transform(lambda x: x.fillna(x.mean()))
print("Group-wise mean filling:")
print(grouped_filled)
```

---

## 6. Data Transformation and Manipulation

### 6.1 Adding and Modifying Columns

```python
# Sample DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'Age': [25, 30, 35, 28],
    'Salary': [50000, 60000, 70000, 55000]
})

# Adding new columns
df['Bonus'] = df['Salary'] * 0.1  # 10% bonus
df['Total_Compensation'] = df['Salary'] + df['Bonus']
df['Age_Group'] = df['Age'].apply(lambda x: 'Young' if x < 30 else 'Senior')

print("DataFrame with new columns:")
print(df)
print()

# Conditional column creation with np.where
df['Performance'] = np.where(df['Salary'] > 60000, 'High', 'Standard')
print("Conditional column with np.where:")
print(df)
print()

# Multiple conditions with np.select
conditions = [
    df['Age'] < 30,
    (df['Age'] >= 30) & (df['Age'] < 35),
    df['Age'] >= 35
]
choices = ['Junior', 'Mid-level', 'Senior']
df['Level'] = np.select(conditions, choices, default='Unknown')
print("Multiple conditions with np.select:")
print(df)
```

### 6.2 Applying Functions

```python
# Apply function to single column
def salary_category(salary):
    if salary < 55000:
        return 'Low'
    elif salary < 65000:
        return 'Medium'
    else:
        return 'High'

df['Salary_Category'] = df['Salary'].apply(salary_category)
print("Applied function to column:")
print(df[['Name', 'Salary', 'Salary_Category']])
print()

# Apply lambda function
df['Name_Length'] = df['Name'].apply(lambda x: len(x))
print("Lambda function application:")
print(df[['Name', 'Name_Length']])
print()

# Apply function to multiple columns
def full_description(row):
    return f"{row['Name']} ({row['Age']} years) earns ${row['Salary']:,}"

df['Description'] = df.apply(full_description, axis=1)
print("Function applied to multiple columns:")
print(df[['Description']])
print()

# Map function for value replacement
age_mapping = {25: 'Twenty-five', 30: 'Thirty', 35: 'Thirty-five', 28: 'Twenty-eight'}
df['Age_Text'] = df['Age'].map(age_mapping)
print("Map function for value replacement:")
print(df[['Age', 'Age_Text']])
```

### 6.3 String Operations

```python
# Create DataFrame with string data
string_df = pd.DataFrame({
    'Names': ['  Alice Smith  ', 'bob jones', 'CHARLIE BROWN', 'diana prince'],
    'Emails': ['alice@email.com', 'bob@EMAIL.COM', 'charlie@Email.Com', 'diana@email.com']
})

print("Original string data:")
print(string_df)
print()

# String cleaning operations
string_df['Names_Clean'] = (string_df['Names']
                           .str.strip()                    # Remove whitespace
                           .str.title())                   # Title case

string_df['Emails_Lower'] = string_df['Emails'].str.lower()  # Lowercase

print("Cleaned string data:")
print(string_df)
print()

# String extraction and manipulation
string_df['First_Name'] = string_df['Names_Clean'].str.split().str[0]
string_df['Last_Name'] = string_df['Names_Clean'].str.split().str[1]
string_df['Domain'] = string_df['Emails_Lower'].str.split('@').str[1]

print("Extracted string components:")
print(string_df[['First_Name', 'Last_Name', 'Domain']])
print()

# Pattern matching with regex
phone_data = pd.DataFrame({
    'Contact': ['123-456-7890', '(555) 123-4567', '555.123.4567', 'invalid']
})

# Extract digits only
phone_data['Digits_Only'] = phone_data['Contact'].str.extract(r'(\d{3}).*(\d{3}).*(\d{4})')
print("Regex pattern extraction:")
print(phone_data)
```

### 6.4 Data Type Conversions

```python
# Sample data with mixed types
mixed_df = pd.DataFrame({
    'Numbers_as_Strings': ['1', '2', '3', '4'],
    'Floats_as_Strings': ['1.5', '2.7', '3.14', '4.8'],
    'Dates_as_Strings': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'],
    'Categories': ['A', 'B', 'A', 'C']
})

print("Original data types:")
print(mixed_df.dtypes)
print()

# Convert string numbers to numeric
mixed_df['Numbers_as_Strings'] = pd.to_numeric(mixed_df['Numbers_as_Strings'])
mixed_df['Floats_as_Strings'] = mixed_df['Floats_as_Strings'].astype(float)

# Convert strings to datetime
mixed_df['Dates_as_Strings'] = pd.to_datetime(mixed_df['Dates_as_Strings'])

# Convert to categorical
mixed_df['Categories'] = mixed_df['Categories'].astype('category')

print("After type conversions:")
print(mixed_df.dtypes)
print()
print(mixed_df)
print()

# Handle conversion errors
error_data = pd.Series(['1', '2', 'invalid', '4'])
converted_safe = pd.to_numeric(error_data, errors='coerce')  # Invalid becomes NaN
print("Safe numeric conversion:")
print(converted_safe)
```

---

## 7. Grouping and Aggregation

### 7.1 Basic Grouping Operations

```python
# Sample sales data
sales_data = pd.DataFrame({
    'Date': pd.date_range('2024-01-01', periods=20, freq='D'),
    'Salesperson': ['Alice', 'Bob', 'Charlie', 'Alice', 'Bob'] * 4,
    'Region': ['North', 'South', 'East', 'West', 'North'] * 4,
    'Product': ['A', 'B', 'A', 'C', 'B'] * 4,
    'Sales': np.random.randint(100, 1000, 20),
    'Quantity': np.random.randint(1, 10, 20)
})

print("Sales data sample:")
print(sales_data.head(10))
print()

# Basic grouping by single column
sales_by_person = sales_data.groupby('Salesperson')['Sales'].sum()
print("Total sales by salesperson:")
print(sales_by_person)
print()

# Multiple aggregation functions
sales_stats = sales_data.groupby('Salesperson')['Sales'].agg(['sum', 'mean', 'count', 'std'])
print("Sales statistics by salesperson:")
print(sales_stats)
print()

# Grouping by multiple columns
region_product_sales = sales_data.groupby(['Region', 'Product'])['Sales'].sum()
print("Sales by region and product:")
print(region_product_sales)
```

### 7.2 Advanced Aggregation

```python
# Custom aggregation functions
def sales_range(series):
    return series.max() - series.min()

def top_quartile_mean(series):
    return series.quantile(0.75)

# Apply custom aggregations
custom_agg = sales_data.groupby('Salesperson')['Sales'].agg([
    'sum',
    'mean',
    ('range', sales_range),
    ('top_quartile', top_quartile_mean)
])
print("Custom aggregation functions:")
print(custom_agg)
print()

# Different aggregations for different columns
multi_column_agg = sales_data.groupby('Region').agg({
    'Sales': ['sum', 'mean'],
    'Quantity': ['sum', 'max'],
    'Salesperson': 'count'
})
print("Different aggregations by column:")
print(multi_column_agg)
print()

# Named aggregations (more readable)
named_agg = sales_data.groupby('Region').agg(
    total_sales=('Sales', 'sum'),
    avg_sales=('Sales', 'mean'),
    total_quantity=('Quantity', 'sum'),
    unique_salespeople=('Salesperson', 'nunique')
)
print("Named aggregations:")
print(named_agg)
```

### 7.3 Transform and Filter Operations

```python
# Transform: apply function but maintain original DataFrame shape
sales_data['Sales_Normalized'] = sales_data.groupby('Region')['Sales'].transform(
    lambda x: (x - x.mean()) / x.std()
)

print("Sales with regional normalization:")
print(sales_data[['Region', 'Sales', 'Sales_Normalized']].head(10))
print()

# Add group statistics as new columns
sales_data['Region_Avg_Sales'] = sales_data.groupby('Region')['Sales'].transform('mean')
sales_data['Sales_vs_Regional_Avg'] = sales_data['Sales'] - sales_data['Region_Avg_Sales']

print("Sales vs regional average:")
print(sales_data[['Region', 'Sales', 'Region_Avg_Sales', 'Sales_vs_Regional_Avg']].head(10))
print()

# Filter groups based on group properties
high_volume_regions = sales_data.groupby('Region').filter(lambda x: x['Sales'].sum() > 5000)
print("Regions with total sales > 5000:")
print(high_volume_regions['Region'].unique())
print()

# Cumulative operations within groups
sales_data['Cumulative_Sales'] = sales_data.groupby('Salesperson')['Sales'].cumsum()
sales_data['Rolling_Avg_Sales'] = sales_data.groupby('Salesperson')['Sales'].rolling(window=3).mean().reset_index(0, drop=True)

print("Cumulative and rolling statistics:")
print(sales_data[['Salesperson', 'Sales', 'Cumulative_Sales', 'Rolling_Avg_Sales']].head(15))
```

### 7.4 Pivot Tables and Cross-tabulation

```python
# Pivot table - Excel-like functionality
pivot_sales = sales_data.pivot_table(
    values='Sales',
    index='Salesperson',
    columns='Region',
    aggfunc='sum',
    fill_value=0
)
print("Pivot table - Sales by Salesperson and Region:")
print(pivot_sales)
print()

# Multiple values in pivot table
pivot_multi = sales_data.pivot_table(
    values=['Sales', 'Quantity'],
    index='Salesperson',
    columns='Region',
    aggfunc={'Sales': 'sum', 'Quantity': 'mean'},
    fill_value=0
)
print("Multi-value pivot table:")
print(pivot_multi)
print()

# Cross-tabulation for categorical data
crosstab = pd.crosstab(
    sales_data['Salesperson'],
    sales_data['Product'],
    values=sales_data['Sales'],
    aggfunc='sum',
    margins=True  # Include totals
)
print("Cross-tabulation with margins:")
print(crosstab)
```

---

## 8. Merging and Joining

### 8.1 Different Types of Joins

```python
# Sample DataFrames for joining
employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'department': ['IT', 'HR', 'IT', 'Finance', 'Marketing']
})

salaries = pd.DataFrame({
    'emp_id': [1, 2, 3, 6, 7],
    'salary': [50000, 55000, 60000, 65000, 70000],
    'bonus': [5000, 5500, 6000, 6500, 7000]
})

print("Employees DataFrame:")
print(employees)
print("\nSalaries DataFrame:")
print(salaries)
print()

# Inner join - only matching records
inner_join = pd.merge(employees, salaries, on='emp_id', how='inner')
print("Inner join:")
print(inner_join)
print()

# Left join - all records from left DataFrame
left_join = pd.merge(employees, salaries, on='emp_id', how='left')
print("Left join:")
print(left_join)
print()

# Right join - all records from right DataFrame
right_join = pd.merge(employees, salaries, on='emp_id', how='right')
print("Right join:")
print(right_join)
print()

# Outer join - all records from both DataFrames
outer_join = pd.merge(employees, salaries, on='emp_id', how='outer')
print("Outer join:")
print(outer_join)
```

### 8.2 Advanced Merging Techniques

```python
# Merging on different column names
departments = pd.DataFrame({
    'dept_name': ['IT', 'HR', 'Finance', 'Marketing'],
    'manager': ['John', 'Jane', 'Mike', 'Sarah'],
    'budget': [100000, 80000, 120000, 90000]
})

# Merge with different column names
dept_merge = pd.merge(
    employees,
    departments,
    left_on='department',
    right_on='dept_name',
    how='left'
)
print("Merge with different column names:")
print(dept_merge)
print()

# Merging on multiple columns
sales_detail = pd.DataFrame({
    'emp_id': [1, 1, 2, 2, 3],
    'quarter': ['Q1', 'Q2', 'Q1', 'Q2', 'Q1'],
    'sales': [10000, 12000, 8000, 9000, 15000]
})

targets = pd.DataFrame({
    'emp_id': [1, 1, 2, 2, 3],
    'quarter': ['Q1', 'Q2', 'Q1', 'Q2', 'Q1'],
    'target': [9000, 11000, 7500, 8500, 14000]
})

multi_merge = pd.merge(sales_detail, targets, on=['emp_id', 'quarter'])
multi_merge['target_achieved'] = multi_merge['sales'] >= multi_merge['target']
print("Multi-column merge:")
print(multi_merge)
print()

# Merge with suffixes for overlapping columns
df1 = pd.DataFrame({'id': [1, 2, 3], 'value': [10, 20, 30]})
df2 = pd.DataFrame({'id': [1, 2, 4], 'value': [100, 200, 400]})

suffix_merge = pd.merge(df1, df2, on='id', how='outer', suffixes=('_left', '_right'))
print("Merge with suffixes:")
print(suffix_merge)
```

### 8.3 Concatenation

```python
# Vertical concatenation (stacking DataFrames)
df_2023 = pd.DataFrame({
    'month': ['Jan', 'Feb', 'Mar'],
    'sales': [1000, 1100, 1200],
    'year': [2023, 2023, 2023]
})

df_2024 = pd.DataFrame({
    'month': ['Jan', 'Feb', 'Mar'],
    'sales': [1050, 1150, 1250],
    'year': [2024, 2024, 2024]
})

vertical_concat = pd.concat([df_2023, df_2024], ignore_index=True)
print("Vertical concatenation:")
print(vertical_concat)
print()

# Horizontal concatenation
personal_info = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
})

contact_info = pd.DataFrame({
    'email': ['alice@email.com', 'bob@email.com', 'charlie@email.com'],
    'phone': ['123-456-7890', '234-567-8901', '345-678-9012']
})

horizontal_concat = pd.concat([personal_info, contact_info], axis=1)
print("Horizontal concatenation:")
print(horizontal_concat)
print()

# Concatenation with keys
data_dict = {
    '2023': df_2023,
    '2024': df_2024
}

keyed_concat = pd.concat(data_dict, names=['year_key', 'row_id'])
print("Concatenation with keys:")
print(keyed_concat)
```

### 8.4 Join Operations on Index

```python
# DataFrames with meaningful indices
left_df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
}, index=['X', 'Y', 'Z'])

right_df = pd.DataFrame({
    'C': [7, 8, 9],
    'D': [10, 11, 12]
}, index=['X', 'Y', 'W'])

# Join on index
index_join = left_df.join(right_df, how='outer')
print("Join on index:")
print(index_join)
print()

# Multiple DataFrame joins
third_df = pd.DataFrame({
    'E': [13, 14, 15]
}, index=['X', 'Z', 'W'])

multi_join = left_df.join([right_df, third_df], how='outer')
print("Multiple DataFrame join:")
print(multi_join)
```

---

## 9. Reshaping and Pivoting

### 9.1 Melting DataFrames

```python
# Wide format data
wide_data = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Math': [85, 90, 78],
    'Science': [88, 85, 92],
    'English': [90, 88, 85]
})

print("Wide format data:")
print(wide_data)
print()

# Melt to long format
long_data = pd.melt(
    wide_data,
    id_vars=['Name'],
    value_vars=['Math', 'Science', 'English'],
    var_name='Subject',
    value_name='Score'
)

print("Melted to long format:")
print(long_data)
print()

# Partial melting
partial_melt = pd.melt(
    wide_data,
    id_vars=['Name'],
    value_vars=['Math', 'Science'],  # Only some columns
    var_name='STEM_Subject',
    value_name='STEM_Score'
)

print("Partial melting:")
print(partial_melt)
```

### 9.2 Pivoting DataFrames

```python
# Pivot long format back to wide
pivoted_back = long_data.pivot(
    index='Name',
    columns='Subject',
    values='Score'
)

print("Pivoted back to wide format:")
print(pivoted_back)
print()

# Reset index to make it a regular column
pivoted_reset = pivoted_back.reset_index()
print("Pivoted with reset index:")
print(pivoted_reset)
print()

# Pivot with multiple values
sales_long = pd.DataFrame({
    'Date': ['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02'],
    'Product': ['A', 'B', 'A', 'B'],
    'Sales': [100, 150, 120, 160],
    'Quantity': [10, 15, 12, 16]
})

# This would create multiple columns for each value
# For multiple values, use pivot_table instead
multi_pivot = sales_long.pivot_table(
    index='Date',
    columns='Product',
    values=['Sales', 'Quantity'],
    aggfunc='sum'
)

print("Multi-value pivot table:")
print(multi_pivot)
```

### 9.3 Stack and Unstack Operations

```python
# Create hierarchical DataFrame
hierarchical_data = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [5, 6, 7, 8],
    'C': [9, 10, 11, 12]
}, index=pd.MultiIndex.from_tuples([
    ('Group1', 'X'), ('Group1', 'Y'), ('Group2', 'X'), ('Group2', 'Y')
], names=['Group', 'Item']))

print("Hierarchical DataFrame:")
print(hierarchical_data)
print()

# Stack - pivot columns to rows
stacked = hierarchical_data.stack()
print("Stacked DataFrame:")
print(stacked)
print()

# Unstack - pivot rows to columns
unstacked = stacked.unstack()
print("Unstacked back:")
print(unstacked)
print()

# Unstack specific level
unstacked_level = hierarchical_data.unstack(level='Group')
print("Unstacked specific level:")
print(unstacked_level)
```

### 9.4 Advanced Reshaping

```python
# Cross-section and selection in MultiIndex
print("Cross-section selection:")
print(hierarchical_data.xs('Group1', level='Group'))
print()

# Swapping levels in MultiIndex
swapped = hierarchical_data.swaplevel('Group', 'Item').sort_index()
print("Swapped levels:")
print(swapped)
print()

# Reshaping with multiple columns
complex_data = pd.DataFrame({
    'Date': ['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02'],
    'Store': ['A', 'B', 'A', 'B'],
    'Product': ['X', 'X', 'Y', 'Y'],
    'Sales': [100, 150, 200, 250],
    'Costs': [80, 120, 160, 200]
})

# Pivot with multiple indices
complex_pivot = complex_data.pivot_table(
    index=['Date', 'Store'],
    columns='Product',
    values=['Sales', 'Costs'],
    fill_value=0
)

print("Complex pivot with multiple indices:")
print(complex_pivot)
```

---

## 10. Time Series Analysis

### 10.1 DateTime Fundamentals

```python
# Creating datetime data
dates = pd.date_range('2024-01-01', periods=10, freq='D')
print("Date range:")
print(dates)
print()

# Different frequencies
monthly_dates = pd.date_range('2024-01-01', periods=12, freq='M')
print("Monthly dates:")
print(monthly_dates)
print()

# Business days only
business_dates = pd.date_range('2024-01-01', periods=10, freq='B')
print("Business days:")
print(business_dates)
print()

# Time series DataFrame
ts_data = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=100, freq='D'),
    'value': np.random.randn(100).cumsum(),
    'category': np.random.choice(['A', 'B', 'C'], 100)
})

# Set date as index
ts_data.set_index('date', inplace=True)
print("Time series DataFrame:")
print(ts_data.head())
print()
print("Index type:", type(ts_data.index))
```

### 10.2 Time Series Indexing and Selection

```python
# Date-based selection
print("Data for January 2024:")
print(ts_data['2024-01'])
print()

# Specific date range
print("Data for first week:")
print(ts_data['2024-01-01':'2024-01-07'])
print()

# Recent data
print("Last 5 days:")
print(ts_data.tail())
print()

# Boolean indexing with dates
recent_data = ts_data[ts_data.index > '2024-02-01']
print(f"Data after Feb 1: {len(recent_data)} records")
```

### 10.3 Resampling and Frequency Conversion

```python
# Create higher frequency data
hourly_data = pd.DataFrame({
    'timestamp': pd.date_range('2024-01-01', periods=168, freq='H'),  # 1 week hourly
    'temperature': 20 + 5 * np.sin(np.arange(168) * 2 * np.pi / 24) + np.random.normal(0, 1, 168),
    'humidity': 50 + 10 * np.cos(np.arange(168) * 2 * np.pi / 24) + np.random.normal(0, 2, 168)
})
hourly_data.set_index('timestamp', inplace=True)

print("Hourly data sample:")
print(hourly_data.head())
print()

# Resample to daily averages
daily_avg = hourly_data.resample('D').mean()
print("Daily averages:")
print(daily_avg)
print()

# Different aggregations
daily_stats = hourly_data.resample('D').agg({
    'temperature': ['mean', 'min', 'max'],
    'humidity': ['mean', 'std']
})
print("Daily statistics:")
print(daily_stats)
print()

# Upsampling (increasing frequency)
daily_sample = hourly_data.resample('D').mean()
upsampled = daily_sample.resample('12H').interpolate()
print("Upsampled to 12-hourly:")
print(upsampled.head(10))
```

### 10.4 Time Series Analysis Operations

```python
# Rolling window operations
ts_data['rolling_mean_7'] = ts_data['value'].rolling(window=7).mean()
ts_data['rolling_std_7'] = ts_data['value'].rolling(window=7).std()

print("Rolling statistics:")
print(ts_data[['value', 'rolling_mean_7', 'rolling_std_7']].head(10))
print()

# Expanding window (cumulative)
ts_data['expanding_mean'] = ts_data['value'].expanding().mean()
ts_data['expanding_std'] = ts_data['value'].expanding().std()

print("Expanding statistics:")
print(ts_data[['value', 'expanding_mean', 'expanding_std']].head(10))
print()

# Percentage change and differences
ts_data['pct_change'] = ts_data['value'].pct_change()
ts_data['diff_1'] = ts_data['value'].diff()
ts_data['diff_7'] = ts_data['value'].diff(7)  # Week-over-week change

print("Changes and differences:")
print(ts_data[['value', 'pct_change', 'diff_1', 'diff_7']].head(10))
print()

# Seasonal decomposition simulation
trend = np.arange(100) * 0.1
seasonal = 5 * np.sin(np.arange(100) * 2 * np.pi / 12)  # 12-period seasonality
noise = np.random.normal(0, 1, 100)
synthetic_ts = pd.Series(trend + seasonal + noise, 
                        index=pd.date_range('2024-01-01', periods=100, freq='D'))

print("Synthetic time series components:")
print(f"Original series (first 10): {synthetic_ts.head(10).tolist()}")
```

### 10.5 Time Zone Handling

```python
# Create timezone-aware data
utc_dates = pd.date_range('2024-01-01', periods=5, freq='H', tz='UTC')
print("UTC dates:")
print(utc_dates)
print()

# Convert to different timezone
ny_dates = utc_dates.tz_convert('US/Eastern')
print("New York timezone:")
print(ny_dates)
print()

# Working with naive and aware datetimes
naive_ts = pd.Series(range(5), index=pd.date_range('2024-01-01', periods=5, freq='H'))
aware_ts = naive_ts.tz_localize('US/Pacific')

print("Timezone localized series:")
print(aware_ts)
```

---

## 11. Statistical Operations

### 11.1 Descriptive Statistics

```python
# Generate sample data for statistical analysis
np.random.seed(42)
stats_data = pd.DataFrame({
    'normal': np.random.normal(100, 15, 1000),
    'uniform': np.random.uniform(0, 100, 1000),
    'exponential': np.random.exponential(2, 1000),
    'integers': np.random.randint(1, 101, 1000)
})

# Basic descriptive statistics
print("Descriptive statistics:")
print(stats_data.describe())
print()

# Additional statistics
print("Additional statistics:")
print(f"Skewness:\n{stats_data.skew()}")
print(f"\nKurtosis:\n{stats_data.kurtosis()}")
print(f"\nMedian:\n{stats_data.median()}")
print(f"\nMode:\n{stats_data.mode().iloc[0]}")
print()

# Quantiles
print("Quantiles:")
quantiles = [0.1, 0.25, 0.5, 0.75, 0.9]
print(stats_data.quantile(quantiles))
```

### 11.2 Correlation and Covariance

```python
# Correlation analysis
correlation_matrix = stats_data.corr()
print("Correlation matrix:")
print(correlation_matrix)
print()

# Specific correlation methods
print("Pearson correlation (default):")
print(stats_data.corr(method='pearson')['normal']['uniform'])
print()

print("Spearman correlation (rank-based):")
print(stats_data.corr(method='spearman')['normal']['uniform'])
print()

print("Kendall correlation:")
print(stats_data.corr(method='kendall')['normal']['uniform'])
print()

# Covariance matrix
covariance_matrix = stats_data.cov()
print("Covariance matrix:")
print(covariance_matrix)
```

### 11.3 Statistical Tests and Operations

```python
# Sample data for hypothesis testing concepts
group_a = np.random.normal(100, 15, 100)
group_b = np.random.normal(105, 15, 100)

test_data = pd.DataFrame({
    'group_a': group_a,
    'group_b': group_b
})

# Basic comparison statistics
print("Group comparison:")
print(f"Group A mean: {test_data['group_a'].mean():.2f}")
print(f"Group B mean: {test_data['group_b'].mean():.2f}")
print(f"Difference: {test_data['group_b'].mean() - test_data['group_a'].mean():.2f}")
print()

# Variance and standard deviation
print("Variance and Standard Deviation:")
print(f"Group A var: {test_data['group_a'].var():.2f}, std: {test_data['group_a'].std():.2f}")
print(f"Group B var: {test_data['group_b'].var():.2f}, std: {test_data['group_b'].std():.2f}")
print()

# Percentile-based analysis
print("Percentile analysis:")
percentiles = [10, 25, 50, 75, 90]
for p in percentiles:
    print(f"{p}th percentile - A: {np.percentile(test_data['group_a'], p):.2f}, "
          f"B: {np.percentile(test_data['group_b'], p):.2f}")
```

### 11.4 Advanced Statistical Operations

```python
# Rolling correlations
time_series_1 = pd.Series(np.random.randn(100).cumsum(), 
                         index=pd.date_range('2024-01-01', periods=100))
time_series_2 = pd.Series(np.random.randn(100).cumsum(), 
                         index=pd.date_range('2024-01-01', periods=100))

rolling_corr = time_series_1.rolling(window=30).corr(time_series_2)
print("Rolling correlation (30-day window):")
print(rolling_corr.tail(10))
print()

# Statistical aggregations by groups
grouped_stats = pd.DataFrame({
    'category': np.random.choice(['A', 'B', 'C'], 300),
    'value1': np.random.normal(100, 15, 300),
    'value2': np.random.normal(50, 10, 300)
})

group_statistics = grouped_stats.groupby('category').agg({
    'value1': ['count', 'mean', 'std', 'min', 'max'],
    'value2': ['mean', 'median', 'var']
})

print("Grouped statistics:")
print(group_statistics)
print()

# Rank operations
stats_data['normal_rank'] = stats_data['normal'].rank()
stats_data['normal_pct_rank'] = stats_data['normal'].rank(pct=True)

print("Ranking operations:")
print(stats_data[['normal', 'normal_rank', 'normal_pct_rank']].head(10))
```

---

## 12. Performance Optimization

### 12.1 Memory Management

```python
# Memory usage analysis
large_df = pd.DataFrame({
    'int_col': np.random.randint(0, 100, 100000),
    'float_col': np.random.randn(100000),
    'string_col': np.random.choice(['A', 'B', 'C', 'D'], 100000),
    'date_col': pd.date_range('2020-01-01', periods=100000, freq='H')
})

print("Memory usage before optimization:")
print(large_df.info(memory_usage='deep'))
print()

# Optimize data types
optimized_df = large_df.copy()

# Convert integers to smaller types
optimized_df['int_col'] = pd.to_numeric(optimized_df['int_col'], downcast='integer')

# Convert strings to categories
optimized_df['string_col'] = optimized_df['string_col'].astype('category')

print("Memory usage after optimization:")
print(optimized_df.info(memory_usage='deep'))
print()

# Memory comparison
original_memory = large_df.memory_usage(deep=True).sum()
optimized_memory = optimized_df.memory_usage(deep=True).sum()
savings = (original_memory - optimized_memory) / original_memory * 100

print(f"Memory savings: {savings:.1f}%")
```

### 12.2 Efficient Data Operations

```python
# Vectorized operations vs loops
data_size = 100000
test_data = pd.DataFrame({
    'A': np.random.randn(data_size),
    'B': np.random.randn(data_size)
})

# Timing vectorized operations
import time

# Vectorized approach (recommended)
start_time = time.time()
test_data['C_vectorized'] = test_data['A'] + test_data['B']
vectorized_time = time.time() - start_time

print(f"Vectorized operation time: {vectorized_time:.4f} seconds")

# Using .apply() efficiently
start_time = time.time()
test_data['C_apply'] = test_data.apply(lambda row: row['A'] + row['B'], axis=1)
apply_time = time.time() - start_time

print(f"Apply operation time: {apply_time:.4f} seconds")
print(f"Vectorized is {apply_time/vectorized_time:.1f}x faster")
print()

# Efficient string operations
string_data = pd.Series(['apple', 'banana', 'cherry'] * 10000)

# Vectorized string operation
start_time = time.time()
result_vectorized = string_data.str.upper()
vectorized_str_time = time.time() - start_time

# Using apply for string operations (less efficient)
start_time = time.time()
result_apply = string_data.apply(lambda x: x.upper())
apply_str_time = time.time() - start_time

print(f"Vectorized string operation: {vectorized_str_time:.4f} seconds")
print(f"Apply string operation: {apply_str_time:.4f} seconds")
```

### 12.3 Query Optimization

```python
# Efficient filtering techniques
large_dataset = pd.DataFrame({
    'id': range(1000000),
    'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], 1000000),
    'value': np.random.randn(1000000),
    'date': pd.date_range('2020-01-01', periods=1000000, freq='H')
})

# Method 1: Boolean indexing (fast)
start_time = time.time()
result1 = large_dataset[large_dataset['category'] == 'A']
method1_time = time.time() - start_time

# Method 2: Query method (readable and often fast)
start_time = time.time()
result2 = large_dataset.query("category == 'A'")
method2_time = time.time() - start_time

# Method 3: Using loc (explicit)
start_time = time.time()
result3 = large_dataset.loc[large_dataset['category'] == 'A']
method3_time = time.time() - start_time

print(f"Boolean indexing: {method1_time:.4f} seconds")
print(f"Query method: {method2_time:.4f} seconds") 
print(f"Loc method: {method3_time:.4f} seconds")
print()

# Index optimization
# Setting appropriate index for frequent lookups
indexed_df = large_dataset.set_index('category')

start_time = time.time()
result_indexed = indexed_df.loc['A']
indexed_time = time.time() - start_time

print(f"Indexed lookup: {indexed_time:.4f} seconds")
```

### 12.4 Chunking and Lazy Loading

```python
# Simulating chunked processing for large files
def process_large_file_chunks(filename, chunksize=10000):
    """
    Example of processing large files in chunks
    """
    processed_results = []
    
    # This would be used with actual file reading:
    # for chunk in pd.read_csv(filename, chunksize=chunksize):
    #     processed_chunk = process_chunk(chunk)
    #     processed_results.append(processed_chunk)
    
    # Simulation with generated data
    total_rows = 100000
    for start_idx in range(0, total_rows, chunksize):
        end_idx = min(start_idx + chunksize, total_rows)
        
        # Generate chunk
        chunk = pd.DataFrame({
            'id': range(start_idx, end_idx),
            'value': np.random.randn(end_idx - start_idx)
        })
        
        # Process chunk (example: compute summary statistics)
        chunk_summary = {
            'chunk_start': start_idx,
            'chunk_size': len(chunk),
            'mean_value': chunk['value'].mean(),
            'std_value': chunk['value'].std()
        }
        
        processed_results.append(chunk_summary)
    
    return pd.DataFrame(processed_results)

# Example usage
chunk_results = process_large_file_chunks('dummy_file.csv')
print("Chunked processing results:")
print(chunk_results.head())
print()

# Memory-efficient aggregations
print("Memory-efficient operations:")
print("Use specific columns only:")
# Instead of: df.groupby('category')['value'].mean()
# Use: df[['category', 'value']].groupby('category')['value'].mean()

print("Use appropriate data types from the start")
print("Consider using categorical data for repeated strings")
print("Use chunked processing for files larger than available RAM")
```

---

## 13. Best Practices and Common Pitfalls

### 13.1 Code Style and Conventions

```python
# Good practices for Pandas code

# 1. Use meaningful variable names
employee_data = pd.DataFrame({
    'employee_name': ['Alice', 'Bob', 'Charlie'],
    'department': ['IT', 'HR', 'Finance'],
    'annual_salary': [50000, 55000, 60000]
})

# 2. Chain operations for readability
processed_data = (employee_data
                 .query('annual_salary > 52000')
                 .assign(monthly_salary=lambda x: x['annual_salary'] / 12)
                 .sort_values('monthly_salary', ascending=False)
                 .reset_index(drop=True))

print("Chained operations result:")
print(processed_data)
print()

# 3. Use vectorized operations instead of loops
# Good: Vectorized
employee_data['salary_category'] = np.where(
    employee_data['annual_salary'] > 55000, 
    'High', 
    'Standard'
)

# Avoid: Looping through rows
# for idx, row in employee_data.iterrows():
#     if row['annual_salary'] > 55000:
#         employee_data.loc[idx, 'salary_category'] = 'High'
#     else:
#         employee_data.loc[idx, 'salary_category'] = 'Standard'

print("Vectorized operation result:")
print(employee_data)
```

### 13.2 Common Pitfalls and How to Avoid Them

```python
# Pitfall 1: SettingWithCopyWarning
print("Pitfall 1: SettingWithCopyWarning")

# This might cause a warning:
# subset = employee_data[employee_data['department'] == 'IT']
# subset['bonus'] = 5000  # Warning!

# Better approach:
subset = employee_data[employee_data['department'] == 'IT'].copy()
subset['bonus'] = 5000
print("Safe subset modification:")
print(subset)
print()

# Pitfall 2: Chained indexing
print("Pitfall 2: Chained indexing")

# Avoid: df[condition][column] = value
# Better: df.loc[condition, column] = value

# Good example:
employee_data.loc[employee_data['department'] == 'IT', 'tech_bonus'] = 2000
print("Safe conditional assignment:")
print(employee_data)
print()

# Pitfall 3: Implicit data type conversions
print("Pitfall 3: Data type awareness")

mixed_data = pd.DataFrame({
    'numbers': [1, 2, 3, 4, 5],
    'strings': ['1', '2', '3', '4', '5']
})

print("Original data types:")
print(mixed_data.dtypes)

# Explicit conversion is better than implicit
mixed_data['strings_as_int'] = mixed_data['strings'].astype(int)
print("After explicit conversion:")
print(mixed_data.dtypes)
print()

# Pitfall 4: Index alignment issues
print("Pitfall 4: Index alignment")

df1 = pd.DataFrame({'A': [1, 2, 3]}, index=[0, 1, 2])
df2 = pd.DataFrame({'A': [4, 5, 6]}, index=[1, 2, 3])

# Addition aligns by index, not position
result = df1 + df2
print("Index-aligned addition:")
print(result)
print("Note: Index 0 and 3 become NaN due to no alignment")
print()

# If you want position-based operation:
result_values = df1.values + df2.values  # NumPy arrays ignore index
print("Position-based addition (values only):")
print(result_values)
```

### 13.3 Performance Best Practices

```python
# Performance tips with examples

# 1. Use vectorized operations
print("Performance Best Practices:")
print("1. Vectorized operations are faster")

large_series = pd.Series(np.random.randn(100000))

# Fast: Vectorized
start_time = time.time()
result_vectorized = large_series.apply(lambda x: x**2 if x > 0 else 0)
vectorized_time = time.time() - start_time

# Even faster: Pure vectorized with numpy
start_time = time.time()
result_numpy = np.where(large_series > 0, large_series**2, 0)
numpy_time = time.time() - start_time

print(f"Vectorized apply: {vectorized_time:.4f} seconds")
print(f"NumPy where: {numpy_time:.4f} seconds")
print(f"NumPy is {vectorized_time/numpy_time:.1f}x faster")
print()

# 2. Use appropriate data structures
print("2. Choose appropriate data structures")

# For categorical data, use 'category' dtype
categorical_data = pd.Series(['A', 'B', 'C'] * 10000)
print(f"String series memory: {categorical_data.memory_usage(deep=True)} bytes")

categorical_optimized = categorical_data.astype('category')
print(f"Categorical series memory: {categorical_optimized.memory_usage(deep=True)} bytes")
print(f"Memory reduction: {(1 - categorical_optimized.memory_usage(deep=True)/categorical_data.memory_usage(deep=True))*100:.1f}%")
print()

# 3. Use built-in methods when available
print("3. Use built-in methods")

sample_df = pd.DataFrame({
    'group': ['A', 'B', 'A', 'B', 'A'] * 1000,
    'value': np.random.randn(5000)
})

# Fast: Built-in groupby
start_time = time.time()
result_builtin = sample_df.groupby('group')['value'].mean()
builtin_time = time.time() - start_time

print(f"Built-in groupby: {builtin_time:.4f} seconds")
print("Always prefer pandas built-in methods over custom implementations")
```

### 13.4 Debugging and Troubleshooting

```python
# Common debugging techniques

debug_df = pd.DataFrame({
    'A': [1, 2, np.nan, 4, 5],
    'B': ['x', 'y', 'z', 'w', 'v'],
    'C': [1.1, 2.2, 3.3, 4.4, 5.5]
})

print("Debugging Techniques:")
print("1. Inspect data structure and types")
print(f"Shape: {debug_df.shape}")
print(f"Columns: {debug_df.columns.tolist()}")
print(f"Data types:\n{debug_df.dtypes}")
print(f"Memory usage:\n{debug_df.memory_usage(deep=True)}")
print()

print("2. Check for missing values")
print(f"Missing values per column:\n{debug_df.isnull().sum()}")
print(f"Total missing values: {debug_df.isnull().sum().sum()}")
print()

print("3. Sample data inspection")
print("First few rows:")
print(debug_df.head(3))
print("\nLast few rows:")
print(debug_df.tail(3))
print("\nRandom sample:")
print(debug_df.sample(2, random_state=42))
print()

print("4. Statistical overview")
print(debug_df.describe(include='all'))
print()

print("5. Check for duplicates")
print(f"Duplicate rows: {debug_df.duplicated().sum()}")
print(f"Duplicate values in column A: {debug_df['A'].duplicated().sum()}")
```

### 13.5 Testing and Validation

```python
# Data validation examples

def validate_dataframe(df, expected_columns=None, expected_types=None):
    """
    Validate DataFrame structure and content
    """
    validation_results = {
        'is_valid': True,
        'issues': []
    }
    
    # Check if DataFrame is empty
    if df.empty:
        validation_results['issues'].append("DataFrame is empty")
        validation_results['is_valid'] = False
    
    # Check expected columns
    if expected_columns:
        missing_cols = set(expected_columns) - set(df.columns)
        if missing_cols:
            validation_results['issues'].append(f"Missing columns: {missing_cols}")
            validation_results['is_valid'] = False
    
    # Check data types
    if expected_types:
        for col, expected_type in expected_types.items():
            if col in df.columns:
                if df[col].dtype != expected_type:
                    validation_results['issues'].append(
                        f"Column '{col}' has type {df[col].dtype}, expected {expected_type}"
                    )
                    validation_results['is_valid'] = False
    
    # Check for excessive missing values (>50%)
    missing_pct = (df.isnull().sum() / len(df)) * 100
    high_missing = missing_pct[missing_pct > 50]
    if not high_missing.empty:
        validation_results['issues'].append(
            f"Columns with >50% missing values: {high_missing.to_dict()}"
        )
    
    return validation_results

# Example validation
test_df = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', None, 'Diana'],
    'age': [25, 30, 35, None],
    'salary': [50000.0, 60000.0, 70000.0, 80000.0]
})

validation_result = validate_dataframe(
    test_df,
    expected_columns=['id', 'name', 'age', 'salary'],
    expected_types={'id': 'int64', 'salary': 'float64'}
)

print("Validation Results:")
print(f"Is valid: {validation_result['is_valid']}")
if validation_result['issues']:
    print("Issues found:")
    for issue in validation_result['issues']:
        print(f"  - {issue}")
```

### 13.6 Advanced Tips and Tricks

```python
# Advanced pandas techniques

# 1. Method chaining with assign
print("Advanced Techniques:")
print("1. Method chaining with assign")

result = (pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
          .assign(C=lambda x: x['A'] + x['B'])
          .assign(D=lambda x: x['C'] * 2)
          .query('D > 10'))

print(result)
print()

# 2. Using pipe for custom functions
def add_percentage_columns(df, base_col):
    total = df[base_col].sum()
    return df.assign(**{f'{base_col}_pct': df[base_col] / total * 100})

sales_df = pd.DataFrame({
    'product': ['A', 'B', 'C'],
    'sales': [100, 200, 300]
})

result = sales_df.pipe(add_percentage_columns, 'sales')
print("2. Using pipe for custom functions:")
print(result)
print()

# 3. Efficient conditional operations
print("3. Efficient conditional operations with np.select:")

conditions = [
    result['sales'] < 150,
    result['sales'] < 250,
    result['sales'] >= 250
]

choices = ['Low', 'Medium', 'High']

result['sales_category'] = np.select(conditions, choices, default='Unknown')
print(result)
print()

# 4. Working with MultiIndex efficiently
print("4. MultiIndex operations:")

multi_df = pd.DataFrame({
    'A': [1, 2, 3, 4, 5, 6],
    'B': [10, 20, 30, 40, 50, 60]
}, index=pd.MultiIndex.from_tuples([
    ('X', 1), ('X', 2), ('X', 3), ('Y', 1), ('Y', 2), ('Y', 3)
], names=['group', 'item']))

# Efficient selection
print("MultiIndex selection:")
print(multi_df.loc['X'])  # All items in group X
print()
print(multi_df.xs(2, level='item'))  # All groups for item 2
```

---

## Conclusion

This comprehensive tutorial covers the essential aspects of the Pandas library, from basic data structures to advanced optimization techniques. Here are the key takeaways:

### Core Concepts Mastered:
- **Data Structures**: Series and DataFrame creation and manipulation
- **Data I/O**: Reading from and writing to various file formats
- **Data Selection**: Boolean indexing, loc/iloc operations
- **Data Cleaning**: Handling missing values and data type conversions
- **Data Transformation**: Applying functions, string operations, and reshaping
- **Grouping and Aggregation**: GroupBy operations and statistical analysis
- **Merging and Joining**: Combining datasets efficiently
- **Time Series**: Working with temporal data and resampling
- **Performance**: Memory optimization and efficient operations

### Best Practices Emphasized:
1. **Use vectorized operations** instead of loops
2. **Choose appropriate data types** to save memory
3. **Handle missing values** explicitly
4. **Use method chaining** for readable code
5. **Validate data** regularly during analysis
6. **Profile performance** for large datasets

### Next Steps:
- Practice with real-world datasets
- Explore visualization with matplotlib/seaborn
- Learn integration with scikit-learn for machine learning
- Study advanced topics like categorical data and sparse arrays
- Contribute to the pandas community

### Resources for Further Learning:
- [Official Pandas Documentation](https://pandas.pydata.org/docs/)
- [Pandas Cookbook](https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html)
- [10 Minutes to Pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html)
- [Pandas Performance Tips](https://pandas.pydata.org/pandas-docs/stable/user_guide/enhancingperf.html)

Remember: Pandas is a powerful tool, but mastery comes through practice. Start with simple operations and gradually work towards more complex data manipulation tasks. Happy data wrangling!
