#1 Palindrome 
import re

def is_palindrome(s: str) -> bool:
    s = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return s == s[::-1]

print(is_palindrome("racecar"))
print(is_palindrome("A man a plan a canal Panama"))

#string

def is_valid_parentheses(s: str) -> bool:
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    for ch in s:
        if ch in pairs.values():
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
        else:
            return False
    return not stack
print(is_valid_parentheses("()"))
print(is_valid_parentheses("()[]{}"))





