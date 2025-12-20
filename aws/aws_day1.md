## Concept questions

1.  Why can’t traditional single-node databases (e.g., MySQL/PostgreSQL) handle Big Data workloads?
Single-node databases scale vertically and quickly hit CPU, memory, storage, and I/O limits, while Big Data workloads require horizontal scaling across many distributed nodes.
    
2. What problems do distributed systems solve, and what new challenges do they introduce?
Distributed systems solve scalability, performance, and fault tolerance, but introduce new challenges like network unreliability, consistency problems, hard transactions, complex debugging, and higher operational overhead.

3. Compare OLTP and OLAP systems. What are their design goals(online transaction/ analytical processing)
OLTP is optimized for fast, concurrent transactional workloads with strict consistency, while OLAP is optimized for large-scale analytical queries and historical reporting using de-normalized, read-optimized schemas.

4. Describe the differences between ETL and ELT. Why is ELT more commonly used in cloud-based architectures such as AWS?
ETL transforms data before loading, while ELT loads raw data first and transforms it inside the data warehouse. ELT is preferred in cloud architectures because cloud warehouses (Redshift, Snowflake, BigQuery) offer cheap storage, massive parallel compute, simpler pipelines, and better scalability.

5. Explain the MapReduce execution flow in your own words. What are the roles of the Map, Shuffle, and Reduce phases?
MapReduce works by mapping raw data into key-value pairs, shuffling the data so identical keys are grouped together across the cluster, and reducing each group to produce the final aggregated output.
Map → extract & emit key–value pairs
Shuffle → sort & group by key (redistribute data)
Reduce → aggregate grouped values

6. Explain the difference between Data Lake and Data Warehouse.
A data lake stores raw data in any format for flexible processing (schema-on-read), while a data warehouse stores cleaned, structured, curated data optimized for fast analytical queries (schema-on-write).

7. What is the difference between Batch Processing and Streaming Processing? Give one real-world use case for each.
Batch processing analyzes large datasets periodically with high latency, while streaming processing handles data continuously in real time; e.g., daily sales summaries (batch) vs. real-time fraud detection (streaming).

8. What is the purpose of Star Schema and Snowflake Schema in data warehousing? Which one is generally preferred for BI workloads, and why?
Both schemas model data for analytics, but star schema uses denormalized dimensions while snowflake schema normalizes them.
 Star schema is preferred for BI because it requires fewer joins, offers faster queries, is easier to understand, and aligns well with OLAP engines and BI tools.



