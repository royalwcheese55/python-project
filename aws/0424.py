'''
1. garbage collection use reference counting and cycle detector for circular 
reference
when object count = 0 memory free

2. threads is a true parallelism and limit by GIL and it is good for 
CPU and blocking IO
coroutines is async is good for single-thread, and IO bound task

3. create index on frequently filtered columns and query patterns

more index will have faster reads but slower writes. 
avoid over- indexing

4.  startup run once when app starts(db connect)
shutdown is a cleanup (close the database)

5. we could import backgroundtasks and def the task with @app.get

6.  pk is unique and not null
unique index is unique but nullable
non-unique allows duplicates

uuid is 16 unit which is too random and may cause fragmentation and slower
inserts

7. transaction is a group of operations executed together
hardest is isolation because concurrent transactions conflict


'''

def longest(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)

    dp = [[0] * (n+1) for _ in range(m+1)]

    for i in range(1, m+1):
        for j in range(1, n+1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]

print(longest('abc', 'abc'))

'''
select name, department, salary
from (select *, dense_rank() over (partition by department order by salary desc)rnk,
count(*) over ( partition by department) cnt from employees)t
where rnk = 2 or cnt = 1;
'''