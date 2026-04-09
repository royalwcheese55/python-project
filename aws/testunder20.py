import time
import threading
from collections  import defaultdict, OrderedDict
from typing import Any, Optional

class TTLCache:
    def __init__(self, max_size=1000, default_ttl=60):
        self.store = OrderedDict()
        self.lock = threading.Lock()
        self.max_size = max_size
        self.default_ttl = default_ttl

    def _is_expired(self,key):
        value, expire_time = self.store.get(key, (None, 0))
        return time.time() > expire_time
    
    def get(self, key):
        with self.lock:
            if key not in self.store:
                return None
            
            if self. _is_expired(key):
                del self.store[key]
                return None
            
            value, _ = self.store.pop(key)
            self.store[key] = (value, time.time() + self.default_ttl)
            return value
        
    def set(self, key, value, ttl = None):
        with self.lock:
            if key in self.store:
                self.store.pop(key)

            if len(self.store) >= self.max_size:
                self.store.popitem(last=False)

            expire_time = time.time() + (ttl or self.default_ttl)
            self.store[key] = (value, expire_time)

    def celanup(self):
        with self.lock:
            keys_to_delete = [k for k in self.store if self. _is_expired(k)]
            for k in keys_to_delete:
                del self.store[k]


class Ratelimiter:
    def __init__(self, limit=100, window=60):
        self.limit = limit
        self.window = window
        self.request = defaultdict(list)
        self.lock = threading.Lock()

    def allow(self,key):
        now = time.time()

        with self.lock:
            timestamps = self.request[key]

            while timestamps and timestamps[0] <= now - self.window:
                timestamps.pop(0)

            if len(timestamps) < self.limit:
                timestamps.append(now)
                return True
            else:
                return False
            
class TaskQueue:
    def __init__(self):
        self.tasks = []
        self.lock = threading.Lock()
        self.running = True
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def add_task(self, func, *args, **kwargs):
        with self.lock:
            self.tasks.append((func, args, kwargs))

    def _worker(self):
        while self.running:
            task = None

            with self.lock:
                if self.tasks:
                    task = self.tasks.pop(0)

            if task:
                func, args, kwargs = task
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    print("Task error:", e)
            else:
                time.sleep(0.1)

    def stop(self):
        self.running = False
        self.thread.join()

class BackendService:
    def __init__(self):
        self.cache = TTLCache(max_size = 500, default_ttl=30)
        self.rate_limiter = Ratelimiter(limit=5, window=10)
        self.queue = TaskQueue()

        self.cleaner_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleaner_thread.start()

    def _cleanup_loop(self):
        while True:
            time.sleep(5)
            self.cache.cleanup()
    
    def handle_request(self, user_id, key):
        if not self.rate_limiter.allow(user_id):
            return {"status": "error", "message":"Rate limit exceeded"}
        
        cached = self.cache.get(key)
        if cached:
            return {"status": "ok", "data": cached, "source": "cache"}
        
        result = self._expensive_operation(key)

        self.cache.set(key, result)
        return {"status": "ok", "data": result, "source": "db"}
    
    def _expensive_operation(self,key):
        time.sleep(0.2)
        return f"value_for_{key}"
    
    def async_log(self, message):
        self.queue.add_task(self._log, message)

    def _log(self, message):
        print(f"[LOG] {message}")

def simulate_request():
    service = BackendService()
    user = "user_1"

    for i in range(10):
        response = service.handle_request(user, "item_1")
        print(i, response)

        service.async_log(f"Request {i} processed")

        time.sleep(1)

if __name__ == "__main__":
    simulate_request()

    

    


