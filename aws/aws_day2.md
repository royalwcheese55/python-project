## concept question
1. What is Apache Spark, and how does it fit into the big data ecosystem (storage vs compute vs resource management)?
Spark is a distributed compute engine that processes big data, stores nothing itself, and relies on external resource managers like YARN or Kubernetes while reading data from systems like HDFS or S3.

2. Explain lazy evaluation in Spark. Why does Spark delay execution until an actionis called?
Lazy evaluation means Spark does not execute transformations immediately.
Instead, transformations (like map, filter, join) build a logical plan (DAG). Spark waits until it sees the full chain of transformations so it can optimize it. and it avoid unnecessary computation.

3. What is the difference between transformations and actions? What happens internally when an action is triggered?
transformations decide what to do, build a logical plan/DAG, action force spark to execute DAG and return a result, and start the actual computation. 
When an action is triggered, Spark takes the full chain of lazy transformations, builds and optimizes a DAG, generates a physical plan, schedules tasks across the cluster, performs any required shuffles, and executes the computation to produce the final result.

4. What is an RDD? Why are immutability and partitioning important in Spark’sdesign?
An RDD (Resilient Distributed Dataset) is Spark’s core data structure — distributed data processing engine that allows large datasets to be processed in parallel across clusters. it's fault- tolerance
immutability ensures safe parallel execution and lineage recovery, while partitioning enables scalable, parallel processing across the cluster.

5. Explain the execution hierarchy in Spark: Application → Job → Stage → Task. What determines stage boundaries?
Application — your entire Spark program (e.g., a Python script or notebook).
Job — triggered each time you call an action (count, show, collect, etc.).
Stage — a group of transformations that can run without requiring a shuffle.
Task — the smallest unit of work; one task runs per partition in each stage. 
Stage boundaries are created whenever a shuffle is required
A Spark job is split into stages based on where shuffles occur, and each stage is broken into tasks that run per partition.

6. What is the difference between narrow and wide transformations? Why are widetransformations usually more expensive?
Narrow transformations operate within a single partition and are fast, while wide transformations require shuffling data across nodes, making them much more expensive.

7. Explain the roles of Driver and Executor. What kind of work happens on eachside?
The driver plans and coordinates the job (DAG creation, scheduling), while executors run the actual tasks on data partitions and return results.

8. What is the Medallion Architecture (Bronze, Silver, Gold)? What type of data and logic belongs in each layer?
Bronze stores raw ingested data(JSON, CSV, logs, clickstream, IoT data), Silver stores cleaned and standardized data(Fixed schema, parsed fields, typed columns), and Gold stores business-ready, aggregated data used for analytics, BI dashboards, and ML models.(Aggregated tables (KPIs, metrics, cubes))

9. Explain SCD Type 0, Type 1, and Type 2 in simple terms. When would you choose each one?
type0: origin value forever
type1: update only the new data, delete history 
type2: insert new row to preserve data
Type 2 when historical tracking matters, Type 1 when only the latest value matters, and Type 0 for values that should never change.

