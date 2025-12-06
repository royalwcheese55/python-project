# Python Interview Questions & Coding Challenges - Session 10

## Concept Questions

- What's the difference between using requests and httpx for making HTTP calls in FastAPI, and why is httpx preferred in async contexts?
requests → synchronous, blocks the event loop, bad for async FastAPI
httpx → async-compatible, non-blocking, supports concurrency, recommended
FastAPI is async-first → so httpx.AsyncClient is the correct choice for outbound HTTP calls

- What are the key differences in the database URL connection string when migrating from sync SQLAlchemy to async SQLAlchemy, and what driver changes are required for PostgreSQL?
Sync → postgresql+psycopg2://... from sqlalchemy import create_engine
Async → postgresql+asyncpg://... from sqlalchemy.ext.asyncio import create_async_engine

- What is ASGI (Asynchronous Server Gateway Interface) and how does it differ from WSGI?
WSGI is synchronous and handles only traditional HTTP.
ASGI is the asynchronous successor, supporting async I/O, WebSockets, and high-concurrency apps.
FastAPI requires ASGI because it relies on async/await.

- How is FastAPI different from Flask?
FastAPI is asynchronous, Flask is synchronous, fastapi is more recent and high performance with auto validation documenatation while flask is simple and flexible.

- Explain the difference between response_model, response_model_exclude, and response_model_include in FastAPI route decorators. When would you use each?
response_model defines what shape the response must have.  Always. Defines the structure of the response.
response_model_include returns only selected fields from that model.   You want only a few fields (like summary lists).
response_model_exclude returns all fields except the ones listed.   You want most fields but need to hide a couple.

- How do you implement JWT authentication in FastAPI
Login → create JWT → return token → user sends token → verify → allow access

User logs in with username/password.
If credentials are valid, server creates a JWT:
Signed with a secret key
Contains user info (e.g. sub=username)
Has an expiry (exp)
Client stores the token (usually in memory/localStorage).
For each protected request, client sends:
Authorization: Bearer <token>
FastAPI dependency:
Extracts the token
Verifies signature + expiry
Decodes payload
Raises 401 if invalid
Injects current user into route

- How does FastAPI handle synchronous functions differently?
FastAPI detects synchronous def route handlers and runs them in a threadpool so they do not block the main async event loop. This allows sync code to coexist with async code without hurting performance.


## Coding Challenge:
# Continue - FastAPI Task Management with Weather Forecast

