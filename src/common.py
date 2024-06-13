from prisma import Prisma
from typing import TypedDict, cast
from decouple import config
import datetime
import jwt
import time
import bcrypt

# Database Client
db = Prisma()

# API Response Struct
def formatted_reply(error_message: str | None = None, datum = None):
    return {
        "error_message": error_message,
        "result": datum
    }

class JwtPayload(TypedDict):
    iss: str
    aud: str
    sub: int
    iat: float
    exp: float

JWT_SECRET = cast(str, config("JWT_SECRET", default="secret"))

# Sign Json Web Token
def sign_jwt(user_id: int) -> str | None:
    current_time = datetime.datetime.utcnow()
    claims = {
        "iss": "snurt",
        "aud": "user",
        "sub": user_id,
        "iat": current_time,
        "exp": (current_time + datetime.timedelta(minutes=15))
    }
    try:
        return jwt.encode(payload=claims, key=JWT_SECRET, algorithm="HS256")
    except:
        return None

# Decode Json Web Token
def decode_jwt(token: str) -> JwtPayload | None:
    try:
        return jwt.decode(jwt=token, key=JWT_SECRET, algorithms=["HS256"], issuer="snurt", audience="user")
    except:
        return None

# Generate a session in Unix
def create_session() -> float:
    current_time = time.time()
    three_days_later = current_time + (3 * 24 * 60 * 60)
    return three_days_later

# Check if the session expired
def verify_session(session: float) -> bool:
    current_time = time.time()
    return current_time > session

# Hash password
def hash_password(text: str) -> str:
    salt = bcrypt.gensalt()
    bytes = bcrypt.hashpw(text.encode("utf-8"), salt)
    return bytes.decode("utf-8")

# Compare password with hash
def verify_password(text: str, hashed: str) -> bool:
    return bcrypt.checkpw(text.encode("utf-8"), hashed.encode("utf-8"))
