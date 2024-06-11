from sanic import Request, Sanic, Config, json
from prisma import Prisma

def formatted_reply(error_details = None, datum = None):
    return {
        "error_details": error_details,
        "result": datum
    }

async def error_handler(request: Request, exception: Exception):
    message = getattr(exception, "message", "Something Went Wrong")
    status_code = getattr(exception, "status_code", 500)
    return json(
        formatted_reply(error_details=f"{message if message else exception}"),
        status_code
    )

class AppContext:
    db: Prisma

class AppInstance(Sanic): Sanic[Config, AppContext]

class BlueprintRequest(Request): Request[AppInstance, None]
