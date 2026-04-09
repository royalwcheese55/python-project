
def isNumber(s: str) -> bool:
    s = s.strip()

    seen_digit = False
    seen_dot = False
    seen_exp = False

    for i,c in enumerate(s):

        if c.isdigit():
            seen_digit = True

        elif c in ['+', '-']:
            if i != 0 and s[i-1] not in['e', 'E']:
                return False
        
        elif c == '.':
            if seen_dot or seen_exp:
                return False
            seen_dot = True

        elif c in ['e', 'E']:
            if seen_exp or not seen_digit:
                return False
            seen_exp = True
            seen_digit = False

        else:
            return False
        
    return seen_digit


print(isNumber("."))        
print(isNumber("3.14"))    
print(isNumber("2e10"))     
print(isNumber("-.9"))     

