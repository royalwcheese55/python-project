# Python Interview Questions & Coding Challenges - Session 1

## Concept Questions
* What is Python's main characteristic regarding syntax compared to other programming languages?
python uses indentation instead of braces. it's clean and readable

* What are the basic data types available in Python?
integer float boolean str/ set tuple list dict

* Why is indentation important in Python?
it helps py as a readable and clean file and it is syntax requirement, and control the code structure

* What happens when you try to mix incompatible data types in an operation?
typeerror, python requires compatible data type

* What is Git Flow?
a structured branching model that separates development, releases, and fixes to keep code organized and stable. help team develop code.

* Explain the difference between `==` and `is` operators
== check if its the same value/ `is` check if its the same object in memory

* What's the difference between implicit and explicit type conversion?
implicit: python do it automatically/ explicit: you have to do it manually using built in functions

* What's the difference between `if x:` and `if x == True:`?
if x: → checks whether x is truthy (used 99% of the time).
if x == True: → checks if x literally equals the boolean True — rarely needed and less flexible.
---

## Coding Questions

### Coding Problem 1: Palindrome Checker

**Problem:**  
Write a function that checks if a string is a palindrome (reads the same forwards and backwards), ignoring spaces, punctuation, and case.

**Description:**  
A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward and backward. Your function should:
- Ignore spaces
- Ignore punctuation marks
- Be case-insensitive
- Return `True` if the string is a palindrome, `False` otherwise

**Function Signature:**
```python
def is_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome.
    
    Args:
        s (str): Input string to check
    
    Returns:
        bool: True if palindrome, False otherwise
    
    Example:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("A man a plan a canal Panama")
        True
        >>> is_palindrome("hello")
        False
    """
    pass
```
---

### Coding Problem 2: Valid Parentheses

**Problem:**  
Given a string containing just the characters `'(', ')', '{', '}', '[', ']'`, determine if the input string is valid.

**Description:**  
A string is considered valid if:
1. Open brackets must be closed by the same type of brackets
2. Open brackets must be closed in the correct order
3. Every close bracket has a corresponding open bracket of the same type
4. Every open bracket must have a corresponding close bracket

**Function Signature:**
```python
def is_valid_parentheses(s: str) -> bool:
    """
    Check if a string has valid parentheses.
    
    Args:
        s (str): String containing only '(', ')', '{', '}', '[', ']'
    
    Returns:
        bool: True if parentheses are valid, False otherwise
    
    Example:
        >>> is_valid_parentheses("()")
        True
        >>> is_valid_parentheses("()[]{}")
        True
        >>> is_valid_parentheses("(]")
        False
    """
    pass
```