Q1. What concrete performance advantages does FastAPI have compared to Flask or Django?
fastapi is async by default, so it has lower latency and faster throughput, it has a built in openapi for faster debug.

Q2. How does FastAPI achieve high performance internally?
async runs on asgi server so it can handle a lot of concurrently tasks, use pydantic for validation and async endpoints for faster jobs.

Q3. What is Dependency Injection in FastAPI, and why is it useful?
you can inject shared requirement like database session or authorization. it can help with less duplicate code.

Q4. How does Django prevent SQL injection?
Q5. What is Idempotency, and why is it important in APIs and CI/CD systems?
multiple request can only have one single result. it prevent retries or internet failure in apis such as banking system, when you withdraw but experience internet failure. rerun the deployment should not change any state as well.

Q6. How would you optimize a slow SQL query in production?
add indexes and reduce some join or select statement, check i/o as well.

Q7. What are common causes of slow SQL queries even when indexes exist?
low selectivity index, bad join, select *

Q8. Difference between RDS and DynamoDB? When would you choose each?
rds: relational database, consistency database /dynamo: nosql, key-value paired choose when you want massive scalable data.

Q9. What are the core features of GraphQL compared to REST?
graph query language is basically a query system that let you fetch the usable data you want not like rest you have to pick a whole chunk of info. single endpoint with schema.

Q10. What is the N+1 problem in GraphQL, and how do you solve it?
it is when you fetch a piece of info like author and product return a list of author and then it return a list of product, we solve it using dataloader(batching).

Q11. Why do large-scale systems prefer horizontal scaling over vertical scaling?
prevent single end-point failure. vertical scaling on one node is expensive and limited by hardware.

Q12. What problems can horizontal scaling introduce?
data consistency issue, complex debugging.

Q13. What are Master, Core, and Task nodes in an EMR cluster?
master: run cluster coordination
core: run task + store data
task: compute only node

Q14. Why is AWS Lambda not suitable for heavy data processing jobs like Spark or Hadoop?
aws lambda has a limited run time
Q15. When would you choose EMR over Lambda or ECS for data processing?
when you need to manage cluster features like scaling and hdfs.


Coding challenge 
Question1
A transaction is possibly invalid if:
• the amount exceeds $1000, or;
• it occurs within (and including) 60 minutes of another transaction with the same name in 
a different city.
You are given an array of strings transactions where transactions[i] consists of comma￾separated values representing the name, time (in minutes), amount, and city of the transaction.
Return a list of strings transactions that are possibly invalid. You may return the answer in any 
order.
Example 1:
Input: transactions = ["alice,20,800,mtv","alice,50,100,beijing"]
Output: ["alice,20,800,mtv","alice,50,100,beijing"]
Explanation: The first transaction is invalid because second transaction of the same name (alice) 
occurs within 60 minutes and in a different city. Similarly, the second one is invalid because of the 
first.
Example 2:
Input: transactions = ["alice,20,800,mtv","alice,50,1200,mtv"]
Output: ["alice,50,1200,mtv"]
Explanation: The second transaction is invalid because the amount exceeds $1000. The first 
transaction is valid because even though it's within 60 minutes of another transaction by the same 
person, it's in the same city.
Example 3:
Input: transactions = ["alice,20,800,mtv","bob,50,1200,mtv"]
Output: ["bob,50,1200,mtv"]
Explanation: Bob's transaction is invalid because the amount exceeds $1000. Alice's transaction is 
valid.
Question2
You are given an integer n. There are n rooms numbered from 0 to n - 1.
You are given a 2D integer array meetings where meetings[i] = [starti, endi] means a 
meeting will be held during the half-closed time interval [starti, endi). All the values 
of starti are unique.
Meetings are allocated to rooms in the following manner:
1. Each meeting will take place in the unused room with the lowest number.
2. If there are no available rooms, the meeting will be delayed until a room becomes free. The 
delayed meeting should have the same duration as the original meeting.
3. When a room becomes unused, meetings that have an earlier original start time should be 
given the room.
Return the number of the room that held the most meetings. If there are multiple rooms, return the 
room with the lowest number.
Input: n = 2, meetings = [[0,10],[1,5],[2,7],[3,4]]
Output: 0
Explanation:
• At time 0, meeting 0 starts in room 0.
• At time 1, meeting 1 starts in room 1.
• At time 2, meeting 2 is delayed.
• At time 3, meeting 3 is delayed.
• At time 5, meeting 1 finishes. meeting 2 starts in room 1 for the time period [5,10).
• At time 10, meetings 0 and 2 finish. meeting 3 starts in room 0 for the time period [10,11).
Both rooms 0 and 1 held 2 meetings, so we return 0.
Example 2:
Input: n = 3, meetings = [[1,20],[2,10],[3,5],[4,9],[6,8]]
Output: 1
Explanation:
• At time 1, meeting 0 starts in room 0.
• At time 2, meeting 1 starts in room 1.
• At time 3, meeting 2 starts in room 2.
• At time 4, meeting 3 is delayed.
• At time 5, meeting 2 finishes. meeting 3 starts in room 2 for the time period [5,10).
• At time 6, meeting 4 is delayed.
• At time 10, meetings 1 and 3 finish. meeting 4 starts in room 1 for the time period [10,12).
Room 0 held 1 meeting, room 1 held 2 meetings, and room 2 held 2 meetings. Since rooms 
1 and 2 held the most meetings and 1 is smaller than 2, we return 1.