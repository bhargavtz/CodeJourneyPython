
# Python OOP Cheat Sheet

## 1. **Class and Object Basics**
- **Class:** Blueprint for creating objects.
- **Object:** Instance of a class.

```python
class MyClass:
    def __init__(self, attribute1, attribute2):
        self.attribute1 = attribute1
        self.attribute2 = attribute2

    def my_method(self):
        return f"Attributes: {self.attribute1}, {self.attribute2}"

# Creating an object
obj = MyClass("Value1", "Value2")
print(obj.my_method())  # Output: Attributes: Value1, Value2
```

## 2. **Class Attributes and Instance Attributes**
- **Instance Attributes:** Unique to each object.
- **Class Attributes:** Shared among all instances of the class.

```python
class MyClass:
    class_attribute = "I am a class attribute"

    def __init__(self, instance_attribute):
        self.instance_attribute = instance_attribute

# Accessing attributes
obj = MyClass("I am an instance attribute")
print(obj.instance_attribute)  # Output: I am an instance attribute
print(MyClass.class_attribute)  # Output: I am a class attribute
```

## 3. **Methods**
- **Instance Methods:** Operate on instances of the class.
- **Class Methods:** Operate on the class itself; use `@classmethod`.
- **Static Methods:** Independent of the class and instance; use `@staticmethod`.

```python
class MyClass:
    def instance_method(self):
        return "Instance method called"

    @classmethod
    def class_method(cls):
        return "Class method called"

    @staticmethod
    def static_method():
        return "Static method called"

obj = MyClass()
print(obj.instance_method())  # Output: Instance method called
print(MyClass.class_method())  # Output: Class method called
print(MyClass.static_method())  # Output: Static method called
```

## 4. **Inheritance**
- **Inheritance:** A class can inherit attributes and methods from another class.

```python
class ParentClass:
    def parent_method(self):
        return "Parent method called"

class ChildClass(ParentClass):
    def child_method(self):
        return "Child method called"

child_obj = ChildClass()
print(child_obj.parent_method())  # Output: Parent method called
print(child_obj.child_method())  # Output: Child method called
```

## 5. **Overriding Methods**
- **Overriding:** A child class can override a method from its parent class.

```python
class ParentClass:
    def method(self):
        return "Parent method"

class ChildClass(ParentClass):
    def method(self):
        return "Overridden method in Child"

child_obj = ChildClass()
print(child_obj.method())  # Output: Overridden method in Child
```

## 6. **Encapsulation**
- **Encapsulation:** Restricting access to methods and variables. Use `_` for protected attributes and `__` for private attributes.

```python
class MyClass:
    def __init__(self):
        self._protected = "Protected"
        self.__private = "Private"

    def get_private(self):
        return self.__private

obj = MyClass()
print(obj._protected)  # Output: Protected
print(obj.get_private())  # Output: Private
```

## 7. **Polymorphism**
- **Polymorphism:** The ability to use a single interface to represent different underlying forms (data types).

```python
class Animal:
    def sound(self):
        return "Some sound"

class Dog(Animal):
    def sound(self):
        return "Bark"

class Cat(Animal):
    def sound(self):
        return "Meow"

def make_sound(animal):
    print(animal.sound())

dog = Dog()
cat = Cat()

make_sound(dog)  # Output: Bark
make_sound(cat)  # Output: Meow
```

## 8. **Abstract Classes**
- **Abstract Classes:** Cannot be instantiated; meant to be subclassed. Use the `abc` module.

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def sound(self):
        pass

class Dog(Animal):
    def sound(self):
        return "Bark"

dog = Dog()
print(dog.sound())  # Output: Bark
```

## 9. **Multiple Inheritance**
- **Multiple Inheritance:** A class can inherit from more than one class.

```python
class ClassA:
    def method_a(self):
        return "Method from ClassA"

class ClassB:
    def method_b(self):
        return "Method from ClassB"

class ClassC(ClassA, ClassB):
    pass

obj = ClassC()
print(obj.method_a())  # Output: Method from ClassA
print(obj.method_b())  # Output: Method from ClassB
```

## 10. **Magic Methods**
- **Magic Methods:** Special methods with double underscores, used for operator overloading and more.

```python
class MyClass:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"MyClass with value {self.value}"

    def __add__(self, other):
        return self.value + other.value

obj1 = MyClass(10)
obj2 = MyClass(20)

print(str(obj1))  # Output: MyClass with value 10
print(obj1 + obj2)  # Output: 30
```
