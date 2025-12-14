# Python Coding Questions - Session 3: Recursion & Functions

## Concept Questions

* What is a lambda function, and how is it different from a regular function in Python?
lambda is a built in function in python also called anonymous function, it is short and single expressions and it's implicitly returned.

* What is the difference between *args and **kwargs in function definitions?
*args handles extra positional arguments as a tuple, and **kwargs handles extra keyword arguments as a dictionary. it handle named arguments in a function.

* What is LEGB? Explain LEGB rule with a code example
Local-Enclosing-Global-Built in
the order python looks up variable names

x = "global"

def outer():
    x = "enclosing"
    
    def inner():
        x = "local"
        print(x)  # LEGB lookup happens here
    inner()

outer()
output will be local

* What is a closure in Python? How is it different from a regular nested function?
A closure is a nested function that captures variables from its enclosing scope and remembers them even after the outer function has finished executing
different from a normal nested function because it preserves state between calls

* What is the purpose of `if __name__ == "__main__":`?
is used to control the execution of code when a Python file is run directly vs when it is imported as a module.

* Can you modify a global variable inside a function without using the `global` keyword?
No, you can’t reassign a global variable inside a function without using the global keyword — Python treats that variable as local. But you can modify a mutable global object (like a list or dict) without declaring it global, since you’re changing the object’s contents, not the reference.”

* In what order must you define parameters in a function signature?
1️⃣ Positional (or required) arguments  
2️⃣ *args (variable positional arguments)  
3️⃣ Keyword-only arguments  
4️⃣ **kwargs (variable keyword arguments)
def func(a, b, *args, c, d=10, **kwargs):
    print(a, b, args, c, d, kwargs)

* What is the difference between the `global` and `nonlocal` keywords?
global modifies a variable at the module level,
while nonlocal modifies a variable in an enclosing (but non-global) scope.
nonlocal is mainly used inside nested functions, often in closures.”

* What is a common pitfall when using mutable default arguments?
A common pitfall is using a mutable object (like a list or dictionary) as a default argument in a function definition.
Because default arguments are evaluated only once—when the function is defined, not each time it’s called—the same mutable object is reused across all calls.

* What is a higher-order function? Give examples of built-in higher-order functions
is one that either takes another function as input or returns a function as output.
Built-in examples include map(), filter(), reduce(), and sorted().”

---

## Coding Questions
### Coding Problem 1: Fibonacci Sequence with Optimization

**Problem:**  
Write a recursive function to calculate the nth Fibonacci number.

**Description:**  
The Fibonacci sequence is a series of numbers where each number is the sum of the two preceding ones, starting from 0 and 1.
- Sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
- Formula: F(n) = F(n-1) + F(n-2), where F(0) = 0 and F(1) = 1

**Requirements:**
- Must use recursion
- Must be efficient enough to handle large values (e.g., n = 50 or higher) without timing out
- Time complexity should be O(n), not O(2^n)
- Hint: Consider using memoization/caching to optimize your solution

**Function Signature:**
**Problem:** Write a recursive function to calculate the nth Fibonacci number. 
**Description:** The Fibonacci sequence is a series of numbers where each number is the sum of the two preceding ones, starting from 0 and 1. - Sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ... - Formula: F(n) = F(n-1) + F(n-2), where F(0) = 0 and F(1) = 1 
**Requirements:** - Must use recursion - Must be efficient enough to handle large values (e.g., n = 50 or higher) without timing out - Time complexity should be O(n), not O(2^n) - Hint: Consider using memoization/caching to optimize your solution **Function Signature:**
python
def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number using optimized recursion.
    
    Args:
        n: Position in Fibonacci sequence (0-indexed)
    
    Returns:
        The nth Fibonacci number
    
    Example:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(6)
        8
        >>> fibonacci(10)
        55
        >>> fibonacci(50)
        12586269025
    """
    pass

---

## Coding Problem 2: Maximum Value in Nested List

**Problem:**  
Write a recursive function to find the maximum value in a nested list structure of arbitrary depth.

**Description:**  
Given a list that may contain integers and other lists (which may also contain integers and lists), find the maximum integer value at any level of nesting. The list can be nested to any depth.

**Function Signature:**
```python
def find_max_nested(nested_list: list) -> int:
    """
    Find the maximum value in a nested list structure using recursion.
    
    Args:
        nested_list: A list containing integers and/or other nested lists
    
    Returns:
        The maximum integer value found at any nesting level
    
    Example:
        >>> find_max_nested([1, 2, 3, 4, 5])
        5
        
        >>> find_max_nested([1, [2, 3], 4, [5, [6, 7]]])
        7
        
        >>> find_max_nested([[1, 2], [3, [4, [5, 6]]], 7])
        7
        
        >>> find_max_nested([10, [20, [30, [40, [50]]]]])
        50
    """
    pass
```

---

## Coding Problem 3: Reverse String Using Recursion

**Problem:**  
Write a recursive function to reverse a string without using built-in reverse methods, slicing, or any iteration.

**Description:**  
Given a string, reverse it using only recursion. You cannot use:
- String slicing (`s[::-1]`)
- The `reversed()` function
- Any loops (`for`, `while`)
- The `.reverse()` method
- List comprehensions or any iterative constructs

You must solve this purely using recursive function calls.

**Function Signature:**
```python
def reverse_string(s: str) -> str:
    """
    Reverse a string using only recursion (no loops, slicing, or built-in reverse).
    
    Args:
        s: Input string to reverse
    
    Returns:
        Reversed string
    
    Example:
        >>> reverse_string("hello")
        "olleh"
        
        >>> reverse_string("Python")
        "nohtyP"
        
        >>> reverse_string("a")
        "a"
        
        >>> reverse_string("")
        ""
        
        >>> reverse_string("racecar")
        "racecar"
    """
    pass
```

---