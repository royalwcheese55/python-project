import time
from collections import deque
from threading import Lock


class SlidingWindowLimiter:
    def __init__(self, limit: int, window: int):
        self.limit = limit
        self.window = window
        self.storage = {}   
        self.lock = Lock()

    def is_allowed(self, user_id: str) -> bool:
        now = time.time()

        with self.lock:
            if user_id not in self.storage:
                self.storage[user_id] = deque()

            q = self.storage[user_id]

            while q and q[0] <= now - self.window:
                q.popleft()

            if len(q) < self.limit:
                q.append(now)
                return True

            return False


limiter = SlidingWindowLimiter(limit=2, window=5)

print(limiter.is_allowed("u1"))  
print(limiter.is_allowed("u1"))  
print(limiter.is_allowed("u1"))  

time.sleep(5)
print(limiter.is_allowed("u1"))  


'''
Deque allows O(1) removal from the front using popleft(), which is perfect for sliding windows. 
A list would require pop(0), which is O(n) and inefficient for frequent operations.

A global lock is simple but blocks all users, creating a bottleneck under high traffic. 
Per-user locks or lock-free approaches improve concurrency and scalability.

In-memory storage won’t work because different servers don’t share state. 

Store timestamps in a sorted set where the score is the timestamp.

'''