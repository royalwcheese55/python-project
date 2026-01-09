# Python Interview Questions & Coding Challenges - Session 8

## Concept Questions

- How does routing work in Flask?
In Flask, routing is the mechanism that maps a URL path to a specific Python function, known as a view function, that handles the web request and returns a response. It is primarily implemented using the @app.route() decorator. 

- What is restful service
a way for different software systems to communicate over the internet using standard HTTP protocols, treating data as "resources" that can be requested and manipulated via URLs and simple commands (GET, POST, PUT, DELETE)

- What are the categories of HTTP status codes (1xx, 2xx, 3xx, 4xx, 5xx)? Provide examples for each.
1xx: Informational 100 continue sending request
2xx: Success 200 success
3xx: Redirect 302 found temp redirect
4xx: Client error 404 not found
5xx: Server error 500 internal server error

- What is HTTP and how does it work
HyperText Transfer Protocol,, communication protocal for transfer data between client and server. client send request and server run backend logic and send back response .

- Explain the concept of idempotency in HTTP methods
idempotency = repeated requests do not change the final result.
GET, PUT, DELETE are idempotent; POST is not.

- Explain the difference between HTTP and HTTPS
http: Data is sent in plain text 
https: secure, encrypted version of HTTP that protects data with TLS/SSL. 
SSL (Secure Sockets Layer) and TLS (Transport Layer Security) are cryptographic protocols that secure internet communication, encrypting data between a user's browser and a website server, preventing eavesdropping, and ensuring data integrity

- Design a RESTful API for a blogging platform
Design resources as /users, /posts, /comments, use standard HTTP verbs for CRUD, JWT for auth, and support pagination/filtering on list endpoints.
The primary resources in a blogging platform are Users, Posts, and Comments. Other potential resources might include Tags, Categories, and Media.

- What is the MVC architecture
model(data and logic) view(ui) controller(user input and request)
design pattern that separates an application into three connected components

- What are Flask's request objects
it holds all information about the client’s HTTP request, including method, headers, parameters, and body.
---

## Coding Challenge:
Create a complete RESTful API for the Customer & Orders model.

```
GET    /api/customers           # Get all customers
GET    /api/customers/<id>      # Get single customer
POST   /api/customers           # Create new customer
PUT    /api/customers/<id>      # Update customer
DELETE /api/customers/<id>      # Delete customer
```

**Customer fields:**
- `id` (Integer, primary key)
- `name` (String, required)
- `email` (String, required, unique)
- `created_at` (DateTime)

```
GET    /api/orders              # Get all orders
GET    /api/orders/<id>         # Get single order
POST   /api/orders              # Create order
PUT    /api/orders/<id>         # Update order
DELETE /api/orders/<id>         # Delete order
```

**Order fields:**
- `id` (Integer, primary key)
- `customer_id` (Integer, foreign key to customers)
- `order_date` (DateTime)
- `total_amount` (Numeric)
- `status` (String, default='pending')

## Requirements
1. Validate required fields
2. Return proper HTTP status codes (200, 201, 404, 400, 500)

---
