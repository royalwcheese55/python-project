1. Why is Redis fast despite being single-threaded?
it is in-memory and no disk, it is a remote dictionary so it uses hash map, so it is a efficient data structures.
single threaded actually avoid lock contention.
2. What is cache consistency, and how is it handled?
cache consistency is keeping the cash and database data aligned.
we use TTL, cache-aside/ write thru/ write behind to handle it.

3. What is Celery, and when would you use it?
task query use for background jobs.
4. What is task idempotency, and why is it important?
running same task multiple times have the same result
important because if we have retries, it prevent duplicate or changes.

5. What is Apache Kafka, and what problems does it solve?
kafka is a distributed event streaming app and it depoule producers/consumers, and real-time pipelines
it gives replayable event history.
6. What are Kafka’s message delivery semantics?
at least once/ at most once/ exactly once

7. How does Kafka differ from traditional message queues?
it is a durable log with replay and consumer offsets. 
multiple consumers can read the same data independently, traditional message queues remove data once consumed.

8. What are indexes and how do they work in databases?
it is data structures that can speed up lookups such as key-value maps. it will have fater reads but extra storage.
9. What are the most common reasons for slow SQL queries?
wrong index/ bad joins/ large aggregate/ slow disk

10. What are Partitioning and Sharding, and what are the main differences?
partition is split data between one database, scaling vertically.
sharding is split data between multiple db servers and scaling horizontally.

11. What’s the difference between continuous integration, continuous delivery, and continuous deployment?
CI: frequent merge and auto test
CD: always deployable and have manual decision
Continuous deployment: every changes passing pipline auto-deploys to production.

12. What is a CI pipeline?
it is an automated steps trigged by code changes from test - build - security checks - package - artifact
13. What is a rollback in CI/CD?
reverting to a secured version of old build when something breaks in current version.
14. What is a deployment strategy?
how do you release safely, rolling, blue-green and shadow deployment
15. What is test-driven development (TDD), and how does it integrate with CI/CD?
write a test and let code pass them first, CI runs on every commit. CD promote the codes that pass.
