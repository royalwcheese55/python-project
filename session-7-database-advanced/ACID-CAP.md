## ACID
![](https://assets.bytebytego.com/diagrams/0407-what-does-acid-mean.png)

### Atomicity
A transaction is all-or-nothing. Either all operations in the transaction complete successfully, or none of them do. If something fails halfway through, everything rolls back to the initial state.

### Consistency
Transactions move the database from one valid state to another, maintaining all defined rules, constraints, and relationships. The database never ends up in an inconsistent state.

### Isolation
Concurrent transactions don't interfere with each other. Each transaction executes as if it's the only one running, even when multiple transactions are happening simultaneously.

### Durability
Once a transaction is committed, it's permanent. Even if the system crashes immediately after, the changes persist


## CAP

### C - Consistency
Every read receives the most recent write or an error. All nodes see the same data at the same time.

| Model | Consistency | Availability | Latency | Use Case |
|-------|-------------|--------------|---------|----------|
| Strong | Highest | Lowest | Highest | Financial systems |
| Eventual | Medium | Highest | Low | Social media |
| Weak | Lowest | Highest | Lowest | Real-time streaming |

### A - Availability
Every request receives a response (success or failure), even if some nodes are down. The system continues operating without complete data.

### P - Partition Tolerance
The system continues to operate despite network partitions (communication breakdowns between nodes). In real distributed systems, partitions will happen, so this is non-negotiable.

![](https://www.researchgate.net/publication/282679529/figure/fig2/AS:614316814372880@1523475950595/sualization-of-CAP-theorem.png)