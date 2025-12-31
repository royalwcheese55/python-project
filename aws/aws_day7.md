Q1. When should you NOT use DynamoDB?
dynamoDB is not relational so it has no foreign key, and no transactions across tables.
it does not support joins and complex filtering, it's max item size is 400kb so no large items like docs or images.

Q2. What causes a hot partition in DynamoDB?
A hot partition in DynamoDB occurs when too many requests are routed to the same partition, overwhelming its capacity while other partitions sit idle. 
1) poor partition key desgin, all trafic hits one partition
2) time-based keys, recent time got hot
3) few keys, uneven distribution.

Q3. How does DynamoDB scale automatically?
dynamodb use data partition and has partition key hash, request are routed by hashing he partition key.
and monitor usage and increase or decrease capacity on demand.

Q4. Difference between RDS and DynamoDB?
RDS(relational database service) is a managed relational database (SQL).  CP(strong consistency)
manage sql db: PostgreSQL, MySQL, Oracle, SQL Server, MariaDB
Data stored in tables with rows and columns/ Strong schema and relationships/ acid compliant/ support joins, transactions etc

DynamoDB is a managed NoSQL key-value / document database. AP(availability)
data accessed thru partition key, no joins/ massive scale and low latency/ serverless

Q5. Explain how the COPY command works in Redshift
it's a data loading mechanism for redshift, it loads large volume of data from S3/dynamoDB or other aws sources, it's cheaper and faster than inserting rows one by one.
COPY sales
FROM 's3://my-bucket/sales/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftRole'
FORMAT AS CSV;

and redshift split file into chunks and distributes them across nodes thats why is fast.

Q6. In one or two sentences, explain the main difference between AWS Glue and Amazon EMR.
AWS Glue is a fully managed, serverless ETL (Extract, Transform, Load) service focused on data integration, while Amazon EMR is a managed cluster platform that provides greater control and flexibility for running a wide variety of big data processing frameworks like Apache Hadoop, Spark, and Presto. 

Q7. What problem does Amazon Athena solve in a data lake?
Querying data without moving it: run SQL directly on data in S3, Schema-on-read: analyze raw data formats (CSV, JSON, Parquet) as-is.

Q8. What are Master, Core, and Task nodes in an EMR cluster?
master: controls the cluster/ manage task like job schdule, resource management and monitoring. one master node
core: Run data processing tasks and store data in HDFS. both compute and storage
task: Run only compute tasks and do not store data in HDFS.



