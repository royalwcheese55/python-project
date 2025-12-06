# Python Interview Questions & Coding Challenges - Session 14

## Concept Questions

- Explain the WebSocket protocol and how it differs from HTTP polling and long polling
websocket: full-time, persistent communication protocol between client and server.
http polling: client repeatedly send request and server have to answer each time
long polling: server holds until new data but client have to reconnect
WebSockets deliver true real-time communication with minimal overhead.

- What caching strategy would you use for frequently accessed but slowly changing data
cache-aside cuz data used very often and does not change fast dont need to read the database every time, also could use TTL to give fresh data and performance.

- Explain the difference between cache-aside, write-through, and write-behind caching patterns
cahce-aside: lazy loading, app check cache first, if miss check db and write into cache. (frequent use, slow changing data)
write-through: on everywrite write to cache, cache sync to db. (strong consistency, like user profile)
write-behind caching: write only goes to cache, cache buffers update, async to db (High-write systems where perfect real-time DB consistency is not critical)
··
- Describe the differences between RabbitMQ, Kafka, and SQS in terms of use cases and guarantees
RabbitMQ → flexible message broker for job queues.
Kafka → high-throughput event streaming with message replay.
SQS → simple managed queue for decoupling services.

- What are message queues and why are they important in distributed systems?
it allow server to communicate efficiently, asynchronously, producer send and message store in queue, consumer process when its ready. it's reliable and scalable.

- How would you implement a retry mechanism with exponential backoff for failed message processing?
I would implement a retry mechanism with exponential backoff by tracking the number of retry attempts for each message, and on failure, re-queue the message with a delay that grows exponentially (e.g., 1s, 2s, 4s, 8s…), up to a max retry limit. After that, I send it to a dead-letter queue. I’d also add jitter to avoid many messages retrying at the same time and make sure the processing is idempotent.

- Explain the concept of dead letter queues and when you'd use them
dlq is a queue that the message sent to when they cant be proccessed after several attempts.
use it when:  You have retry mechanisms, want to prevent message loss, need monitoring and alerting.

- How does FastAPI handle synchronous functions differently?
FastAPI runs sync functions in a separate thread so they don’t block the async event loop.

## Coding Question

# Rate Limiter - Interview Challenge

## Stage 1

Design a Rate Limiter that controls the number of requests per user within a time window.

```python
class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int) -> None:
        pass
    
    def allow_request(self, user_id: str) -> bool:
        pass
```

**Example:**
```python
limiter = RateLimiter(max_requests=3, window_seconds=10)

assert limiter.allow_request("alice") == True   # 1st
assert limiter.allow_request("alice") == True   # 2nd
assert limiter.allow_request("alice") == True   # 3rd
assert limiter.allow_request("alice") == False  # 4th - denied

assert limiter.allow_request("bob") == True     # bob's 1st

# After 10 seconds pass, alice's requests expire
```

---


## Stage 2

Optimize your Stage 1 solution to O(1) time complexity using the Token Bucket Algorithm.

**Hint:** Calculate tokens to add based on elapsed time since last refill.

```python
class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float) -> None:
        pass
    
    def allow_request(self, user_id: str) -> bool:
        pass
```

**Example:**
```python
# capacity=5, refill_rate=2 tokens/sec
limiter = TokenBucketRateLimiter(capacity=5, refill_rate=2)

# Use all 5 tokens
assert limiter.allow_request("alice") == True   # token: 4
assert limiter.allow_request("alice") == True   # token: 3
assert limiter.allow_request("alice") == True   # token: 2
assert limiter.allow_request("alice") == True   # token: 1
assert limiter.allow_request("alice") == True   # token: 0
assert limiter.allow_request("alice") == False  # no tokens

# Wait 1 second, gain 2 tokens
# Now alice can make 2 more requests
```


## Token Bucket Algorithm

**Concept:**
Imagine a bucket that:
- Starts with a maximum capacity of tokens (e.g., 5 tokens)
- Tokens refill at a constant rate (e.g., 2 tokens per second)
- Each request consumes 1 token
- If the bucket is empty, the request is denied
- The bucket never overflows (capped at capacity)

**How it works:**
1. User makes a request
2. Calculate how many tokens to add based on elapsed time since last request
3. Add tokens (up to capacity max)
4. If tokens ≥ 1, allow request and consume 1 token
5. If tokens < 1, deny request

**Visual Example:**

```
Time 0s:   Bucket: ●●●●●  (5 tokens, full)
           Request 1: allowed → Bucket: ●●●●  (4 tokens)
           Request 2: allowed → Bucket: ●●●  (3 tokens)
           Request 3: allowed → Bucket: ●●  (2 tokens)
           Request 4: allowed → Bucket: ●  (1 token)
           Request 5: allowed → Bucket: ○  (0 tokens)
           Request 6: DENIED (no tokens)

Time 0.5s: Elapsed: 0.5 seconds × 2 tokens/sec = 1 new token
           Bucket: ●  (1 token)
           Request 7: allowed → Bucket: ○  (0 tokens)

Time 1.0s: Elapsed: 0.5 seconds × 2 tokens/sec = 1 new token
           Bucket: ●  (1 token)
           Request 8: allowed → Bucket: ○  (0 tokens)

Time 1.5s: Elapsed: 0.5 seconds × 2 tokens/sec = 1 new token
           Bucket: ●  (1 token)
           Request 9: allowed → Bucket: ○  (0 tokens)

Time 2.5s: Elapsed: 1 second × 2 tokens/sec = 2 new tokens
           Bucket: ●●  (2 tokens, not capped)
           Request 10: allowed → Bucket: ●  (1 token)
           Request 11: allowed → Bucket: ○  (0 tokens)
```

**Key Points:**
- Token refill is calculated on-demand (no background process)
- Tokens accumulate based on time elapsed since last request
- Bucket capacity caps the maximum tokens
- Allows controlled bursts (use all tokens at once if needed)
- Per-user state: each user has independent tokens and refill time
