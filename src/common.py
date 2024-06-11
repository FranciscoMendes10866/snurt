from sanic import Request, Sanic, Config, json
from prisma import Prisma

async def error_handler(request: Request, exception: Exception):
    message = getattr(exception, "message", "Something Went Wrong")
    status_code = getattr(exception, "status_code", 500)
    return json(
        {
            "errors": {
                "message": f"{message if message else exception}",
                "exception": f"{exception}",
            }
        },
        status_code,
    )

class AppContext:
    db: Prisma

class AppInstance(Sanic): Sanic[Config, AppContext]

class BlueprintRequest(Request): Request[AppInstance, None]
