# Python Interview Questions & Coding Challenges - Session 15

## Concept Questions

- What's the difference between unit tests, integration tests, and end-to-end tests? When would you use each?
unit: test small piece like a function or method, use when during development and test logic
integration: test multiple components work together like app + db, api + cache, use when testing db interactions.
E2E; entire system for user perspective, use when before release, and verify critical flows.

- Explain the purpose of mocking in unit tests. What's the difference between Mock, MagicMock, and patch in Python's unittest.mock?
used in unit tests to replace real dependencies (DB, API calls, files, network, time, etc.) with fake objects so you can test your code in isolation.
mock is the basic mock set attribute and return value, magicmock is mock with magic methods predefined(__len__, __str__) use when code needs. patch is used to temporarily replace an object at a specific import path during a test such as a function or a class.

- Explain test coverage. What's a good coverage percentage to aim for?
Test coverage is a metric that measures how much of your code is executed when your tests run.
Common types include:
Line coverage → % of lines executed
Branch coverage → % of if/else paths tested
Function coverage → % of functions called
Statement coverage → % of statements executed
80% is a good coverage to aim for

- How do you handle testing code that involves database operations? What strategies can you use to avoid hitting real databases?
eparate unit tests and integration tests.
In unit tests, I avoid hitting a real DB by mocking the database layer (e.g., repository/ORM calls) or using fakes/in-memory stores.
For integration tests, I use a real test database (or in-memory DB) with migrations and roll back transactions after each test.
This keeps unit tests fast and pure, while still verifying the real DB behavior separately.

- What's test-driven development (TDD)?
Test-driven development (TDD) is a software development process where you write tests before writing the actual code, following a tight cycle of:
Red → Green → Refactor.

- Explain the typical stages in a CI/CD pipeline. What happens in each stage?
ci/cd: building/testing/deploying code, it has 5 main stages
1- source/version controal, dev push code to git, pipeline trigger automatically
2- build stage, install dependencies and package application
3- test stage, run unit/integration test and security scans to catch bug early
4- predeploy stage, deploy staging env mimic the production to validate code before go live
5- deploy stage, release code

- What's the purpose of environment variables and secrets management in CI/CD? How do you handle sensitive data?
Environment variables let you configure your application without hard-coding values in code. same code work in different environment
Secrets = sensitive values that must stay private: password, api key, jwt key, cloud credentials, it is to make sure they are encrypted and not stored in code
Never store secrets in the code repo, Use a dedicated secrets manager like github secrets and aws secrets manager, Use environment variables at runtime and restrick access.


- Explain the roles in Scrum: Product Owner, Scrum Master, and Development Team. What are each person's responsibilities?
PO Owns and prioritizes the Product Backlog, Makes decisions about scope, priority, and product direction, decides what features to build and in what order.

SM Ensures the team follows Scrum framework correctly, Removes blockers / impediments ensures the team is productive by teaching Scrum and removing roadblocks.

Dev Build the product (coding, testing, designing, documenting), maintain quality does the actual work and decides how to build the product.


## Coding Challenge: 
## Challenge: Unit Testing, CI/CD, and Deployment for FastAPI Note App

**Description:**

Extend the built the FastAPI "note app" in a previous assignment (see session-11-fast-api-2) with automated unit tests, configure a CI workflow with GitHub Actions, and deploy your app to a public service.

### Requirements

1. **Unit Tests**
    - Write unit tests that cover at least the following:
        - Models: Test creation of `User` and `Note` objects and their relationships.
        - API Endpoints: Test the main CRUD routes (create, read, update, delete notes).
        - Edge Cases: Try invalid input and assert error handling (e.g., duplicate users, unauthorized access).
    - Use `pytest` as your testing framework.
    - Aim for at least **80% code coverage**. Check coverage with `pytest-cov`.

2. **CI with GitHub Actions**
    - Create a `.github/workflows/ci.yaml` workflow file that does the following on every push and pull request:
        - Set up Python.
        - Install dependencies.
        - Run the tests and report coverage.
    - Ensure the workflow fails if tests fail or if coverage drops below your threshold.

3. **Deployment**
    - Deploy your FastAPI app to a public PaaS of your choice. You may use:
        - **Railway** (https://railway.app)
        - **Render** (https://render.com)
        - **Fly.io** (https://fly.io)
        - Or similar free service.
    - The service must be accessible via a public HTTP endpoint.
    - Use secrets for database credentials/API keys in your CI workflow.
