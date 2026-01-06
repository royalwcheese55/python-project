'''
1. What is Django’s MTV architecture and how is it different from MVC?
django mtv is model, template, view. mvc is model view controller which the controller handle the routing. in mtv it is the view do the controller role, view is internally processed.

2. Difference between primary key, unique index, and non-unique index.
pk is a unique identifier of a row, cannot be null. can only have one per table.
unique index is also a unique identifier but it allow null and multipe per table
non-unique it allows duplicate and just for the query.

2.1. Why might it cause some issues if we use UUID as the primary key?
the number is long, too large and it depends sometime it could be good as pk, but the index size can be large.. leading to slower query time. it hurts performance.

3. What is a transaction? Which ACID property is hardest to guarantee and why?
it happens between multiple databases and group different operations into a single unit.
atomicity/consistency/isolation/durability, the hardest should be isolation and durability because stronger isolation require less concurrency. 

4. How does row-level locking work in InnoDB? When can it degrade to table locks?

5. Differences between threading, multiprocessing, and asyncio in Python.
threading shares memory and it is slower, limited by GIL.
multiprocessing runs parallel , it is seperate process, and GIL won't limit it.
asyncio is multitasking for io handeling.

5.1.Which one would you pick in CPU-bound and IO-bound and why?
cpu: multiprocessing because it avoid gil
io: aysnico because it can waits on IO

6. What is the GIL, and why can multiprocessing bypass it?
global interpreter lock, allows only one thread to execute python bytecode.
multiprocessing bypass it because each process has its own interpreter.

7. What does the event loop do? Difference between a coroutine and a task.
event loop schedule and run async operations, coroutine is an function of async definition, task is coroutine executed.

8. Use cases of list vs deque vs heapq.
list: index and iteration
deque: append/pop from both ends
heapq: retrieve min/max elements.

9. Difference between cProfile and line_profiler, and when to use each.

10. Which Python operations look O(1) but are not?
list.remove()

11. Difference between staticmethod, classmethod, and instance method.
classmethod use cls and operate on class state
instance method defines an object. object.method()
staticmethod belong to a class, and it dont need self. it is used for utility logical functions.

12. What is idempotency in REST? Which HTTP methods should be idempotent?
it means multiple request only have one result.
get/put/delete should be idempotent.

13. How does Django ORM prevent SQL injection?

13.1 Difference between select_related and prefetch_related in Django ORM?
select_related: just for sql join
prefetch_related: runs addtional queries and merge result in python

14. What is an API contract and why is it critical?
api contract defines request format, responses, and error behavior, it can let team update system 
indepentently without breaking clients.

15. What problem does FastAPI-style dependency injection solve?
removes duplicated logic and centralize shared concerns like authentication and database sessions.
it uses python typehint and depend()

15.1 Are FastAPI dependencies singleton or request-scoped?
it is request-scoped.

16. What is middleware, and how is it different from an interceptor?


17. How do you implement global exception handling in FastAPI?
by registering a exception handlers. @app.exception_handler.

18. JWT vs session: key differences and why JWT is stateless.
jwt stores state on client side and it is verified cryptographically.
sessions store data on server and requires storage and lookup.

18.1 What's the biggest risk of JWT?
it cannot be revoked easily once its issued.

19. Key design differences between Flask and FastAPI.
fastapi is async first and it is type safety and auto docs
flask is synchronous and it's much simple and flexible.

20. What problems does GraphQL solve compared to REST?
it lets client request exactly what they need, reduce over-fetching.

21. When would you prefer composition over inheritance in Python?
when the behavior or code classes changed often.

22. What does the CAP theorem really state?
consistency/availability/partition tolerance, you can only get two out of three for databases.
and partition tolerance is a must have.

23. What is idempotent retry and why must retries include timeouts?
it retries to prevent some internet faliure, prevent duplicate actions. and timeout prevent stuck request and system failures.

24. What is the purpose of consumer groups in Kafka?

25. What is a circuit breaker and what problem does it solve?
it prevent repeated calls to failing services, protecting system stability.

26. How does the GIL affect concurrent model inference in Python?
threads cannot fully utilize multiple cores so it has to use multiprocessing.

27. Why do AI inference services often use async + batching?
async prevent idling. improve efficiency, batching increase throughput.

28. Why is NumPy faster than Python loops?
it uses a C code and execute vectorized operations, it has a efficient memory layout.

29. What causes cold start issues in model-serving systems?
model-loading, container start-up delays.

30. If an AI API is slow, which layers would you investigate first?
check the model interference first, than hardware usage.


#sql
select name,department,salary
from(select *
     dense_rank()over
(partition by department order by salary desc) as rank from employees)t
where rank <= 2;
'''

#coding
from collections import Counter

def topKFrequent(nums, k):
    freq = Counter(nums)

    buckets = [[]for _ in range(len(nums) + 1)]
    for num, count in freq.items():
        buckets[count].append(num)

    res = []
    for i in range(len(buckets) - 1, 0, -1):
        for n in buckets[i]:
            res.append(n)
            if len(res) == k:
                return res
            
nums = [1, 1, 1, 2, 2, 3]
k = 2
print(topKFrequent(nums, k))
print(topKFrequent([4,4,4,6,6,8], 3))

