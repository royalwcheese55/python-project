## Installing required packages

To install the required packages run in project directory with venv activated:

```bash
uv pip install pyjwt "pwdlib[argon2]" 'pydantic[email]'
```

Install SqlAlchemy async support
```bash
uv pip install asyncpg 'sqlalchemy[asyncio]'
```

Install https for async http client

```bash
uv pip install httpx python-dotenv
```

## start fastapi server

```bash
fastapi dev main.py
```