'''
1. kafka has 3 layers, authorization authentication and encryption

authentication: sasl so producers and consumers log in with username/passwords
authorization: kafka acl control which principal can read/write specific topics
or consumer groups
encryption  just enable tls/ssl

2. first monitor memory growth with metrics like heap usage and gc frequency
then reproduce the issue under load and use profiling tools to identify which
objects keep growing, common issues like unbounded caches and global lists
fix is adding limits and ttls or proper cleanup.

3. target sla expected rps and p95 latency, error rate and throughput then create 
realistic traffic patterns and monitor app / db metrics kafka and cpu error rates
the goal is to find the bottleneck and capacity limit

4.grpc beccause it is low latency and high throughput and it uses http/2
it is smaller and fater than rest, it also supports streaming and strict contracts

5. use cacheaside and when write update the database first then invalidate 
or refresh the cache, also use versioning or timestamps when needed 

6. check row counts sums and sample record comparison.

7. risk in kafka is silent data loss or silent failure, kafka can keep accepting
messages to reduce just monitor consumer lag, lq volume and processing rates
also use idempotent consumers and replay capability

8. timeouts, retries with exponential backoff, circuit breakers and dlqs.
for distributed workflows. avoid one big transaction across services and use 
event-driven design or saga pattern. each should be able to retry safely and 
recover without corrupting

9. consumers safe to process same message more than once. common methods 
are idempotency keys and unique constraints.

10. detect with monitoring and laerts. signals are consumer lag increasing
no offset commits and input rate greater than output rate.

11. kafka is fast because it uses sequential disk write and batching zero-copy
transfer partitioning and consumer groups. producers batch may records and 
consumers read sequentially.

12. at least once means message will not be lost but may processed more than once
exactly once means kafka tries ensure each message affects the output once using
idempotent. and it can be missing

13. use schema registry with avro or json schema, producers and consumers follow rules 
usually backward or forward compatibility. safe changes include adding optional fields

14. rebalance happens when consumers join or leave a consumer group or partitions
change, kafka temporarily reassigns partitions among consumers during this time
consumption may pause.

15. isr means insync replicas
acks = all means all replicas need to acknowledge the message before considering it successful

16. kafka vs rabbimq
kafka is better for high-throughput event streaming log retention and replay
rabbitmq is best for traditional task queues nad request/reply 
it focus on delivering messages to consumers.

17. hashmap store key-value paris, it hashes the key to find a bucket then stores
value there. lookup insert and delete are o(1), if many keys collide performance can degrad

18. remote dictionary server, its a in-memory key-value store, we use it for caching 
rate limiting and it is fast.

19. rate limiting algo: fixed window: count requests in a fixed time window

sliding window: track request over a moving time window, accurate but expensive

token bucket tokens refill at a fixed rate

20. lua script: it let multiple redis commands run automatically, useful when 
logic need read-check write behavior. without lua another cliend could modify 
the key between commands. with lua redis executes the scipt as on operation.

'''


def trap(height: list[int]) -> int:
    left = 0
    right = len(height) - 1

    left_max = 0
    right_max = 0
    water = 0

    while left < right:
        if height[left] < height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1

    return water


# test cases
print(trap([0,1,0,2,1,0,1,3,2,1,2,1]))  # 6
print(trap([4,2,0,3,2,5]))              # 9
print(trap([1,2,3,4]))                  # 0
print(trap([4,3,2,1]))                  # 0