# Python Interview Questions & Coding Challenges - Session 7

## Concept Questions

- What's the difference between a view, materialized view, and a table? When would you use each?
Table → real stored data
View → virtual query, always fresh. a saved SQL query that shows data from base tables.
Materialized View → stored snapshot of a query, faster but needs refresh everytime

- What is ORM? Why do we need ORM?
object relational mapping, lest u use python object to interact with database instead of sql. let you switch between Postgres, MySQL, SQLite without changing code.

- Explain the ACID properties. How do they ensure database reliability?
atomicity: all success or all failed, no partial updates.
consistency: data is always valid
isolation: Transactions don’t interfere with each other.
durability: Data is safe after commit.

- Explain the CAP theorem.
consistency: All nodes see the same data at the same time.
avalability: Every request gets a response, even if it’s not the latest data.
partition tolerance: The system continues working even if network between nodes fails
you can only get two out of three from CAP.

- When would you choose SQL over NoSQL and vice versa?
SQL → structured data, strong consistency, complex queries
NoSQL → flexible schema, high scalability, huge data, fast reads/writes

- What is eventual consistency?
not consistent right now, but guaranteed to become consistent later.

- What are the different consistency models in distributed systems (strong, weak, eventual)?
Strong consistency → always latest data
Weak consistency → no guarantee you'll get the latest data
Eventual consistency → temporarily inconsistent, but guaranteed to converge over time

- Explain the difference between horizontal scaling (scaling out) and vertical scaling (scaling up).
vertical: increase power of a single server, simple to implement.
horizental: high availability and more servers, gets more power and reliability.

- How does MongoDB handle transactions and ACID properties?
MongoDB is always ACID for single-document operations.
Since version 4.0, it supports multi-document, multi-collection ACID transactions.
Transactions come with performance overhead → use them only when necessary.

- What is sharding in databases? How does it differ from partitioning?
Sharding = distributed partitioning across multiple servers. date to different machines for scaling.
Partitioning = splitting data inside the same database or cluster. for organize and performance.
---

## Coding Challenge:
The rest part of the Session 6 Library Management System

---
