from functools import wraps
from sanic import Request, Sanic, Config, SanicException, json
from typing import cast

from .common import formatted_reply, decode_jwt

# API Error Handler
async def error_handler(request: Request, exception: Exception):
    message = getattr(exception, "message", "Something Went Wrong")
    status_code = getattr(exception, "status_code", 500)
    return json(
        formatted_reply(error_message=f"{message if message else exception}"),
        status_code
    )

# Auth Guard
class Context:
    user_id: int

ContextAwareRequest = Request[Sanic[Config, None], Context]

def authorized():
    def decorator(f):
        @wraps(f)
        async def auth_guard(__, request: ContextAwareRequest, *args, **kwargs):
            bearer = cast(str | None, request.headers.get("Authorization", None))
            if not bearer:
                raise SanicException(message="Unauthorized", status_code=401)

            access_token = bearer.replace("Bearer ", "")
            claims = decode_jwt(access_token)
            if not claims:
                raise SanicException(message="Unauthorized", status_code=401)

            request.ctx.user_id = claims["sub"]

            response = await f(__, request, *args, **kwargs)
            return response
        return auth_guard
    return decorator
