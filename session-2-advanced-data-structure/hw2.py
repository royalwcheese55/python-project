# Two Sum Problem
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}  
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
       
print(two_sum([2, 7, 11, 15], 9))  
print(two_sum([3, 2, 4], 6))        
print(two_sum([3, 3], 6))   

#Substring
def length_of_longest_substring(s):
    seen, start, best = {}, 0, 0
    for i, c in enumerate(s):
        if c in seen and seen[c] >= start:
            start = seen[c] + 1
        seen[c], best = i, max(best, i - start + 1)
    return best

print(length_of_longest_substring("abcabcbb"))  
print(length_of_longest_substring("bbbbb"))     
print(length_of_longest_substring("pwwkew"))    


#Array
def product_except_self(nums):
    res = [1] * len(nums)
    prefix = suffix = 1
    for i in range(len(nums)):
        res[i] *= prefix
        prefix *= nums[i]
        res[-1 - i] *= suffix
        suffix *= nums[-1 - i]
    return res
print(product_except_self([1, 2, 3, 4])) 


#Anagram
def group_anagrams(strs):
    from collections import defaultdict
    res = defaultdict(list)
    for w in strs: res["".join(sorted(w))].append(w)
    return list(res.values())

print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
print(group_anagrams(["a"]))
