# Performance optimization strategies

## 0. Most important way to measure / analyze performance
- EXPLAIN ANALYZE
- add Monitors to monitor the querying performance(from third party platform like Datadog)

## 1. Better Index
### Pros
- Dramatic performance improvements (100x-1000x faster)
- Easy to implement (one SQL statement)
- No application changes needed
- Low risk
- Immediate impact

### Cons
- Slower writes (index must be updated on INSERT/UPDATE/DELETE)
- Uses disk space (can be substantial for large tables)
- Too many indexes hurt performance
- Need to maintain/rebuild periodically
- Wrong index doesn't help (or makes things worse)

### When to Use
- **First solution** for slow queries
- Queries scanning many rows
- Frequent WHERE, JOIN, ORDER BY operations
- Before considering more complex solutions

### When NOT to Use
- Table has mostly writes, few reads
- Columns with low cardinality (e.g., boolean fields)
- Already have 5+ indexes on the table
- Query needs full table scan anyway

## 2. Read Replicas
![](https://miro.medium.com/1*NMt7vXbqH34hNJLHVU2d-A.png)
### Pros
- Scales read capacity horizontally (add more replicas)
- Reduces load on primary database
- Improves read latency (replicas closer to users)
- High availability (failover if primary dies)
- Can use replicas for backups, analytics
- Relatively simple to implement
### Cons
- Replication lag (replicas slightly behind primary)
- Application must route reads vs writes
- Doesn't help with write-heavy workloads
- More infrastructure to manage
- Stale reads possible
- Costs (running multiple servers)

### When to Use

- Read-heavy workloads (90%+ reads)
- Primary database CPU maxed out from reads
- Need geographic distribution
- Want high availability
- Analytics queries interfere with production

### When NOT to Use
- Write-heavy workload
- Strong consistency required everywhere
- Single-server can handle current load
- Budget constrained


## 3. Caching
![](https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6939442a-fa84-44ae-8ec7-09c605ae32c9_1804x1494.png)

### Common Tools:
- Redis: In-memory key-value store, pub/sub, data structures
- Memcached: Simple key-value cache

### Pros
- Massive performance improvement (10-100x faster)
- Reduces database load dramatically
- Scales horizontally

### Cons
- Cache invalidation is hard
- Stale data possible
- Added complexity (what to cache, how long, invalidation)

### When to Use

- Read-heavy with frequent repeated queries
- Expensive queries (complex joins, aggregations)
- Hot data (20% of data, 80% of requests)
- High traffic with mostly static data

### When NOT to Use

- Data must always be perfectly fresh
- Write-heavy workload

## 4. Materialized views

### Pros
- Dramatic query speedup (minutes → milliseconds)
- Reduces CPU load and I/O on source tables
- Transparent to application (queries like regular tables)
- Can add indexes for further optimization

### Cons
- Stale data (only current as of last refresh)
- Storage overhead (duplicates data)
- Refresh can be expensive and slow
- Standard refresh blocks queries (use CONCURRENTLY to avoid)

### When to Use:

- Reporting and analytics dashboards
- Complex aggregations run frequently
- Read-heavy workloads where slight staleness is acceptable
- Expensive queries that don't need real-time data

### When NOT to Use:

- You need real-time data
- Data changes very frequently
- The underlying query is already fast
- Storage is limited


## 5. Partitioning
![](https://www.datasunrise.com/wp-content/uploads/2019/09/Partitioning-1.jpg)

### Pros
- Query performance
- Parallel query execution
- Better for time-series data

### Cons
- Increased complexity
- Queries without partition key scan all partitions
- Hard to change partition strategy

### When to Use
- Large tables (>100GB)
- Clear access patterns by date/region/category
- Time-series or log data

### When NOT to Use
- Small tables (<50GB)
- Unpredictable query patterns
- Need flexibility in querying



## 6. Sharding
![](https://substackcdn.com/image/fetch/$s_!vnZu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a8944df-ac2d-4554-be29-bfcb4edcb0c7_1474x1036.png)


### Pros
- Massive scalability (nearly unlimited horizontal scaling)
- Linear scaling for reads AND writes
- Parallel query execution across shards
- Fault isolation (one shard failure doesn't take down entire system)

### Cons
- Massive complexity (application, deployment, operations)
- Cross-shard queries are painful
- No distributed transactions (ACID across shards is hard)
- Aggregations are expensive (query all shards)
- Uneven data distribution (hot shards)
- Rebalancing is HARD (adding/removing shards)
- Can't go back (one-way door decision)

### When to Use
- Massive scale (multi-TB data, 100K+ QPS, hundreds of millions of users)
- Clear, clean shard key (tenant_id, user_id, device_id)
- Write-heavy workload (single database bottlenecked on writes)
- Isolation requirements (enterprise customers, security, performance tiers)

### When NOT to Use
- Premature optimization (database <1TB, <50K QPS)
- No clear shard key (queries filter on different columns)
- Lots of cross-shard queries needed (JOINs, global searches, aggregations)
- Complex transactions (financial transfers, multi-step workflows, need ACID)
- Limited budget (sharding requires significant infrastructure + ops cost)
- Rapid schema changes (startup iterating quickly, finding product-market fit)


## Decision Tree
```
Query is slow?
└─ Add indexes

Database CPU high from reads?
└─ Add read replicas

Same queries repeated frequently?
└─ Add caching
└─ Materialized views

Table very large (>100GB)?
└─ Add partitioning

Need more capacity but not at limits?
└─ Vertical scaling (Increase machine capacity)

Still hitting limits after all above?
└─ Consider sharding (last resort) 
