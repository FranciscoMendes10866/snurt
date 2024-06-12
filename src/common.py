from prisma import Prisma
from sanic import Request, Sanic, Config, json

db = Prisma()

def formatted_reply(error_message: str | None = None, datum = None):
    return {
        "error_message": error_message,
        "result": datum
    }

async def error_handler(request: Request, exception: Exception):
    message = getattr(exception, "message", "Something Went Wrong")
    status_code = getattr(exception, "status_code", 500)
    return json(
        formatted_reply(error_message=f"{message if message else exception}"),
        status_code
    )
