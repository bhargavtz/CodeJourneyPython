
# Python Data Structures Cheat Sheet

## 1. **Lists**
- **List:** Ordered, mutable collection that can hold items of different types.

```python
my_list = [1, 2, 3, "four", [5, 6]]
print(my_list[0])        # Output: 1
print(my_list[-1])       # Output: [5, 6]
my_list.append(7)        # Adds 7 to the end
my_list.remove(2)        # Removes the first occurrence of 2
```

- **Common Methods:**
  - `append(item)`: Adds an item to the end of the list.
  - `remove(item)`: Removes the first occurrence of an item.
  - `pop(index)`: Removes and returns the item at the given index.
  - `sort()`: Sorts the list in ascending order.
  - `reverse()`: Reverses the order of the list.

## 2. **Tuples**
- **Tuple:** Ordered, immutable collection that can hold items of different types.

```python
my_tuple = (1, 2, 3, "four")
print(my_tuple[1])       # Output: 2
```

- **Common Operations:**
  - Accessing elements with indexing: `my_tuple[0]`.
  - Slicing: `my_tuple[1:3]`.
  - Concatenation: `my_tuple + (5, 6)`.

## 3. **Dictionaries**
- **Dictionary:** Unordered collection of key-value pairs.

```python
my_dict = {"name": "Alice", "age": 25}
print(my_dict["name"])   # Output: Alice
my_dict["age"] = 26      # Update value
my_dict["city"] = "NYC"  # Add new key-value pair
```

- **Common Methods:**
  - `get(key)`: Returns the value for the given key.
  - `keys()`: Returns a list of all keys.
  - `values()`: Returns a list of all values.
  - `items()`: Returns a list of (key, value) pairs.
  - `pop(key)`: Removes and returns the value for the given key.

## 4. **Sets**
- **Set:** Unordered, mutable collection of unique elements.

```python
my_set = {1, 2, 3, 4, 5}
my_set.add(6)            # Adds 6 to the set
my_set.remove(3)         # Removes 3 from the set
```

- **Common Methods:**
  - `add(item)`: Adds an item to the set.
  - `remove(item)`: Removes an item from the set.
  - `union(other_set)`: Returns a new set with all elements from both sets.
  - `intersection(other_set)`: Returns a new set with common elements.
  - `difference(other_set)`: Returns a new set with elements in the first set but not in the second.

## 5. **Strings**
- **String:** Immutable sequence of characters.

```python
my_string = "Hello, World!"
print(my_string[1])       # Output: e
print(my_string.lower())  # Output: hello, world!
print(my_string.split(",")) # Output: ['Hello', ' World!']
```

- **Common Methods:**
  - `lower()`: Converts all characters to lowercase.
  - `upper()`: Converts all characters to uppercase.
  - `split(delimiter)`: Splits the string into a list of substrings.
  - `strip()`: Removes leading and trailing whitespace.
  - `find(substring)`: Returns the index of the first occurrence of the substring.
  - `replace(old, new)`: Replaces occurrences of a substring with another substring.

## 6. **Lists vs. Tuples**
- **Lists** are mutable, meaning they can be changed after creation.
- **Tuples** are immutable, meaning they cannot be changed after creation.

```python
my_list = [1, 2, 3]
my_tuple = (1, 2, 3)
my_list[0] = 4           # Allowed
# my_tuple[0] = 4        # Error: Tuple does not support item assignment
```

## 7. **Dictionaries vs. Sets**
- **Dictionaries** store key-value pairs, while **Sets** only store unique values without keys.

```python
my_dict = {"a": 1, "b": 2}
my_set = {1, 2, 3}

# Dictionary example:
print(my_dict["a"])      # Output: 1

# Set example:
my_set.add(4)
print(my_set)            # Output: {1, 2, 3, 4}
```

## 8. **List Comprehensions**
- **List Comprehensions:** A concise way to create lists.

```python
squares = [x**2 for x in range(1, 6)]
print(squares)           # Output: [1, 4, 9, 16, 25]
```

- **Set and Dictionary Comprehensions** follow similar syntax.

```python
# Set comprehension
unique_squares = {x**2 for x in range(1, 6)}
print(unique_squares)    # Output: {1, 4, 9, 16, 25}

# Dictionary comprehension
squared_dict = {x: x**2 for x in range(1, 6)}
print(squared_dict)      # Output: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

## 9. **Iterating Over Data Structures**
- **List:**

```python
for item in my_list:
    print(item)
```

- **Tuple:**

```python
for item in my_tuple:
    print(item)
```

- **Dictionary:**

```python
for key, value in my_dict.items():
    print(f"{key}: {value}")
```

- **Set:**

```python
for item in my_set:
    print(item)
```

## 10. **Nested Data Structures**
- **Lists, dictionaries, and tuples can be nested inside each other.**

```python
nested_list = [[1, 2, 3], [4, 5, 6]]
nested_dict = {"a": {"b": 1, "c": 2}, "d": {"e": 3, "f": 4}}

# Accessing nested structures:
print(nested_list[0][1])  # Output: 2
print(nested_dict["a"]["b"])  # Output: 1
```
