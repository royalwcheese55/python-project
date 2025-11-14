#fibonacci 
from functools import lru_cache

def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(20))

#Max value
def find_max_nested(lst):
    res = float('-inf')
    for x in lst:
        res = max(res, find_max_nested(x) if isinstance(x, list) else x)
    return res

print(find_max_nested([-1000, 0, [1, 2, 3], 1000]))


#reverse string
def reverse_string(s: str) -> str:
    if len(s) <= 1:
        return s
    return reverse_string(s[1:]) + s[0]


    