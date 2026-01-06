## ACID
![](https://assets.bytebytego.com/diagrams/0407-what-does-acid-mean.png)

### Atomicity
A transaction is all-or-nothing. Either all operations in the transaction complete successfully, or none of them do. If something fails halfway through, everything rolls back to the initial state.

### Consistency
Transactions move the database from one valid state to another, maintaining all defined rules, constraints, and relationships. The database never ends up in an inconsistent state.

A banking system has a rule (constraint) that an account balance cannot go below zero (no overdrafts allowed). 
If someone attempts to withdraw $500 from an account that only has $300, the system checks this constraint. Because the withdrawal would violate the business rule, the transaction is disallowed and rolled back, ensuring the database remains in a consistent state where no account holds a negative balance

### Isolation
Isolation ensures that a new transaction, accessing a particular record, waits until the previous transaction finishes before it commences operation. It ensures that concurrent transactions do not interfere with each other

User A finds the last ticket and starts the purchase process. Their transaction (let's call it Transaction A) begins.
Simultaneously, User B also tries to buy a ticket for the same concert. Their transaction (Transaction B) begins. 
Without Isolation:
If there were no isolation, both users might see the "1 ticket available" status, both proceed to the payment stage, and both might successfully complete their purchase because the other's actions weren't hidden. The database would then be in an inconsistent state, having sold two tickets when only one existed. 

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