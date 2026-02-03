'''
1. Given an unsorted integer array nums. Return the smallest positive integer that is not present
in nums. You must implement an algorithm that runs in O(n) time and uses O(1) auxiliary space.
Example 1:
Input: nums = [1,2,0]
Output: 3
Explanation: The numbers in the range [1,2] are all in the array.
Example 2:
Input: nums = [3,4,-1,1]
Output: 2
Explanation: 1 is in the array but 2 is missing.
Example 3:
Input: nums = [7,8,9,11,12]
Output: 1
Explanation: The smallest positive integer 1 is missing.
Constraints:
1 <= nums.length <= 105
-231 <= nums[i] <= 231 - 1
'''
def missingPositive(nums):
    n = len(nums)

    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            idx = nums[i] - 1
            nums[i], nums[idx] = nums[idx], nums[i]

    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    
    return n + 1
print(missingPositive([0, 1, 3, 4]))
'''
2. Given an array of integer citations where citations[i] is the number of citations a researcher
received for their ith paper, return the researcher's h-index.
According to the definition of h-index on Wikipedia: The h-index is defined as the maximum
value of h such that the given researcher has published at least h papers that have each been
cited at least h times.
Example 1:
Input: citations = [3,0,6,1,5]
Output: 3
Explanation: [3,0,6,1,5] means the researcher has 5 papers in total and each of them had
received 3, 0, 6, 1, 5 citations respectively.
Since the researcher has 3 papers with at least 3 citations each and the remaining two with no
more than 3 citations each, their h-index is 3.
Example 2:
Input: citations = [1,3,1]
Output: 1
Example 3:
Input: citations = [9, 7, 6, 2, 1]
Output: 3
Constraints:
n == citations.length
1 <= n <= 5000
0 <= citations[i] <= 1000
'''

