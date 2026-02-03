 q1. What is the difference between CI and CD?
 continuous integration and continuous delivery/deployment
 ci is to keep integrade new code to one repository so that is easy to debug and find issue earlier.
 cd is to automatically deploy the valid code to staging or production.
 Q2. How do you handle rollback in production?
 you immediately rollback to the stable version and using ci/cd for the previous(stable) version, implement green/blue or canary rollout and keep the database migration backward-compatible
 Q3. What’s the difference between blue-green and canary deployment?
 blue-green has two env and two version green is new and blue is old, test the green one and if everything is good then immediately switch to green. canary is to release the new version to a small percentage of users like 5-10% and gradually deploy more if is good.
 Q4. What’s the “testing pyramid” in CI/CD?
 unit- function- e2e
 Q5. How do you handle database migrations in zero-downtime deployment?
 the database must be backward compatible and break down large compatible data to smaller ones.
 Q6. How do you monitor a deployment and decide whether to rollback?
 we check the error rate and the p95/99 latency, and we use some business metrics to see if it's healthy to decide whether to rollback
 Q7. What do you version in a production system?
 we version the entire database schema, code, and dependencies/ documentations like api documentation.
 Q8. Explain Kafka topic, partition, and consumer group.
 kafka topic is key-value paird and it is a log of event, it is append only so that the old log are immutable and the append only so you can only add new log into it, partition is that you split different topics to different partitions so that kafka topics are parrallel and ordered, consumer group are scaled consumption, one consumer per partition.
 Q9. What is consumer lag and how do you monitor it?
 it is a delay of message that the writers wrote it and the consumer cannot see, we use prometheus and kafka metrics to monitor it.
 Q10. What is an offset in Kafka?
 its a unique id assigned to a partition.
 Q11. What causes duplicate messages in Kafka?
 producer retries.
 Q12. Explain Kafka delivery semantics (at-most-once / at-least-once / exactly-once).
 exactly once: idempotent producer
 at-most once: no retries
 at-least once: retries, might be duplicated results
 Q13. How do you handle schema evolution in Kafka events?
 use a schema registry
 Q14. What is a DLQ (Dead Letter Queue) and why is it needed?
 dlq is a letter queue that hold letters that cannot be processed after some retries and it put it to dlq
 it is for error handling and prevents the messages that can't be processed and debug let developer to inspect the cause of faliure.
 Q15. What happens during consumer group rebalance
 it happens when a consumer join group, and there will be a leader selected, and then they assign partitions, and the consumption will be paused in the meantime。

 