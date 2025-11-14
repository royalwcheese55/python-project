#cache
from functools import wraps

def cache_with_log(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))  
        if key in cache:
            print(f"[HIT] Returning cached result for {func.__name__}{args, kwargs}")
            return cache[key]
        else:
            print(f"[MISS] Calling function {func.__name__}{args, kwargs}")
            result = func(*args, **kwargs)
            cache[key] = result
            print(f"[STORE] Cached result for {func.__name__}{args, kwargs}")
            return result

    return wrapper

#generator
def batch(iterable, batch_size):
    current = []
    for item in iterable:
        current.append(item)
        if len(current) == batch_size:
            yield current
            current = []
    if current:      
        yield current
print(list(batch([1, 2, 3, 4, 5, 6, 7], 3)))

#async
import asyncio
import random
from functools import wraps

def async_retry(max_attempts=3, base_delay=1, backoff_factor=2):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 1
            delay = base_delay

            while True:
                try:
                    print(f"[Retry] Attempt {attempt} calling {func.__name__}...")
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt >= max_attempts:
                        print(f"[Retry] All {max_attempts} attempts failed: {e}")
                        raise
                    print(f"[Retry] Error: {e}. Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                    attempt += 1
                    delay *= backoff_factor  # exponential backoff

        return wrapper

    return decorator

