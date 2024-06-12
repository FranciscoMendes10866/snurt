from prisma import Prisma
from sanic import Request, json
from typing import Any, TypedDict, cast
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

# API Error Handler
async def error_handler(request: Request, exception: Exception):
    message = getattr(exception, "message", "Something Went Wrong")
    status_code = getattr(exception, "status_code", 500)
    return json(
        formatted_reply(error_message=f"{message if message else exception}"),
        status_code
    )

class JwtPayload(TypedDict):
    iss: str
    aud: str
    sub: int
    iat: float
    exp: float

JWT_SECRET = cast(str, config("JWT_SECRET", default="secret"))

# Sign Json Web Token
def sign_jwt(user_id: int) -> str:
    claims = {
        "iss": "snurt",
        "aud": "user",
        "sub": user_id,
        "iat": datetime.datetime.utcnow().timestamp(),
        "exp": (datetime.datetime.utcnow() + datetime.timedelta(minutes=15)).timestamp()
    }
    return jwt.encode(payload=claims, key=JWT_SECRET, algorithm="HS256")

# Decode Json Web Token
def decode_jwt(token: str) -> JwtPayload | None:
    try:
        return jwt.decode(jwt=token, key=JWT_SECRET, algorithms=["HS256"])
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
