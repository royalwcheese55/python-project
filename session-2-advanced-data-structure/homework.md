```markdown
# Python Interview Questions & Coding Challenges - Session 2

## Concept Questions

* What is the difference between mutable and immutable data types in Python?
mutable is changable after creation like a list, immutable is unchangable once created.

* What's the difference between a list and a tuple in Python?
List → mutable, uses [sqaure brackes], slower but flexible.
Tuple → immutable, uses (parentheses), faster and safer for fixed data。

* What's the difference between `list.append()`, `list.extend()`, and `list.insert()`?
append: Adds one item to the end of the list.
extend: Adds each element from another iterable (like a list, tuple, or string) to the end of the list. Unlike append(), it doesn’t nest the object — it unpacks it.
insert: Inserts a single item at a specific position.

* Explain the difference between shallow copy and deep copy between `list.copy()`, `list[:]`, and `copy.deepcopy()`
.copy() just duplicate the shells, core is shared, deepcopy() duplicates everything and is fully independent. changes in one do not affect the original list.

* What are the advantages and disadvantages of using set comprehensions vs converting a list comprehension to a set?
set comprehension is slightly faster and more readable and use less memory basically more efficient, the disadvantage is that you can't use the list afterward.

* What's the time complexity difference between checking membership (`in` operator) in a list vs a set?
list use a linear search so O(n) the bigger the list the longer the search.  set use a hash table internally python compute the hash value of x and jump to location so O(1) 

* Why are tuples immutable but you can still modify a list inside a tuple?
Tuple immutability = its structure can’t change. mutable objects stored in a tuple do not lose their mutability e.g. you can still modify inner lists using list methods

* What will `my_list[::2]`, `my_list[::-1]`, and `my_list[1::3]` return for `my_list = [0,1,2,3,4,5,6,7,8,9]`?
02468
9876543210
147

* What's the difference between `remove()`, `pop()`, and `del` for lists?
remove() deletes the first matching value from the list. It searches by value, not index
pop() deletes an element by index and also returns it. If no index is given, it removes and returns the last element.
del is a statement, not a method — it deletes elements or slices by index or range.
---

## Coding Questions

### Coding Problem 1: Two Sum

**Problem:**  
Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.

**Description:**  
You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.

**Function Signature:**
```python
def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Find two numbers that add up to target.
    
    Args:
        nums: List of integers
        target: Target sum
    
    Returns:
        List containing indices of the two numbers
    
    Example:
        >>> two_sum([2, 7, 11, 15], 9)
        [0, 1]
        
        >>> two_sum([3, 2, 4], 6)
        [1, 2]
    """
    pass
```

---

### Coding Problem 2: Longest Substring Without Repeating Characters

**Problem:**  
Given a string `s`, find the length of the longest substring without repeating characters.

**Description:**  
A substring is a contiguous sequence of characters within a string. You need to find the longest substring where all characters are unique (no character appears more than once).

**Function Signature:**
```python
def length_of_longest_substring(s: str) -> int:
    """
    Find length of longest substring without repeating characters.
    
    Args:
        s: Input string
    
    Returns:
        Integer representing the length of longest substring
    
    Example:
        >>> length_of_longest_substring("abcabcbb")
        3  # "abc"
        
        >>> length_of_longest_substring("bbbbb")
        1  # "b"
        
        >>> length_of_longest_substring("pwwkew")
        3  # "wke"
    """
    pass
```

---

### Coding Problem 3: Product of Array Except Self

**Problem:**  
Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`.

**Description:**  
You must write an algorithm that runs in O(n) time and without using the division operation. The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.

**Function Signature:**
```python
def product_except_self(nums: list[int]) -> list[int]:
    """
    Calculate product of array except self.
    
    Args:
        nums: List of integers
    
    Returns:
        List where each element is the product of all other elements
    
    Example:
        >>> product_except_self([1, 2, 3, 4])
        [24, 12, 8, 6]
        # For index 0: 2*3*4 = 24
        # For index 1: 1*3*4 = 12
        # For index 2: 1*2*4 = 8
        # For index 3: 1*2*3 = 6
        
        >>> product_except_self([-1, 1, 0, -3, 3])
        [0, 0, 9, 0, 0]
    """
    pass
```

---

### Coding Problem 4: Group Anagrams

**Problem:**  
Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

**Description:**  
An anagram is a word or phrase formed by rearranging the letters of a different word or phrase, using all the original letters exactly once. For example, "listen" and "silent" are anagrams.

**Function Signature:**
```python
def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Group anagrams together.
    
    Args:
        strs: List of strings
    
    Returns:
        List of lists, where each inner list contains anagrams
    
    Example:
        >>> group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
        
        >>> group_anagrams([""])
        [[""]]
        
        >>> group_anagrams(["a"])
        [["a"]]
    """
    pass
```