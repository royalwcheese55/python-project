# NO-SQL

## Document databases:

MongoDB - Storing user profiles, product catalogs, blog posts where each item has different fields
Couchbase - Mobile app data syncing, content management systems

## Key-Value databases:

Redis - Session storage, caching API responses, real-time leaderboards
DynamoDB - User sessions, shopping carts, game state storage

## Column-family databases:

Cassandra - Time-series data like sensor readings, activity logs, messaging history
HBase - Large-scale analytics, storing massive datasets that need fast writes

## Graph databases:

Neo4j - Social networks, recommendation engines, fraud detection
Amazon Neptune - Knowledge graphs, identity management, network analysis

### Common patterns:

- Use Redis when you need to read something super fast and temporary
- Use MongoDB when your data looks like JSON and changes structure often
- Use Cassandra when you're writing tons of time-stamped data
- Use Neo4j when relationships between things matter more

### Which one to choose?
![](https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad3cb281-2af9-436e-b474-f697368a2049_2250x2624.png)

### Choose SQL when:

- You need data to be correct and consistent (like bank accounts, shopping carts)
- Your data connects together in clear ways (users have orders, orders have products)
- You need to run complicated searches and reports on your data
- Your data structure won't change much over time

### Choose NoSQL when:

- You need to handle huge amounts of data across many servers
- Your data doesn't fit into neat tables or changes shape a lot
- Speed matters more than having the absolute latest data (like social media posts)
- You mostly look up one thing at a time by its ID