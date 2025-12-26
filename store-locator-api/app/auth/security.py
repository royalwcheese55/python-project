import os, time, hashlib
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
ACCESS_MIN = int(os.getenv("ACCESS_TOKEN_MINUTES", "15"))
REFRESH_DAYS = int(os.getenv("REFRESH_TOKEN_DAYS", "7"))

if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET is not set in .env")

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())

def make_access_token(user_id: str, email: str, role: str) -> str:
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_MIN)
    payload = {"user_id": user_id, "email": email, "role": role, "exp": exp}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def make_refresh_token(user_id: str) -> tuple[str, datetime]:
    exp = datetime.utcnow() + timedelta(days=REFRESH_DAYS)
    raw = f"{user_id}:{time.time()}".encode()
    token = hashlib.sha256(raw).hexdigest()
    return token, exp

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])