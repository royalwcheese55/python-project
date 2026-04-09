def findmin(nums):
    l, r = 0, len(nums) - 1

    while l < r:
        mid = (l + r) // 2
        if nums[mid] > nums[r]:
            l = mid + 1
        else:
            r = mid
    return nums[l]

nums = [ 5,6,7,0,1 ]
print(findmin(nums))



def maxAreaOfIsland(grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()

    def dfs(r, c):
        if (r < 0 or r >= rows or
            c < 0 or c >= cols or
            grid[r][c] == 0 or
            (r, c) in visited):
            return 0

        visited.add((r, c))
        return 1 + dfs(r+1,c) + dfs(r-1,c) + dfs(r,c+1) + dfs(r,c-1)

    max_area = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r,c) not in visited:
                max_area = max(max_area, dfs(r,c))

    return max_area


grid = [
  [0,1,1,0,1],
  [1,0,1,0,1],
  [0,1,1,0,1],
  [0,1,0,0,1]
]


print(maxAreaOfIsland(grid))



import heapq
def minInterval(intervals, queries):
    intervals.sort()
    sorted_queries = sorted((q, i) for i, q in enumerate(queries))
    res = [-1] * len(queries)
    heap = []
    i = 0

    for q, idx in sorted_queries:
        while i <len(intervals) and intervals[i][0] <= q:
            l, r = intervals[i]
            heapq.heappush(heap, (r - l + 1, r))
            i += 1

        while heap and heap[0][1] < q:
            heapq.heappop(heap)

        if heap:
            res[idx] = heap[0][0]

    return res

intervals = [[1,3],[2,3],[3,7],[6,6]]
queries = [2,3,1,7,6,8]

print(minInterval(intervals, queries))
# [2, 2, 3, 5, 1, -1]

                            