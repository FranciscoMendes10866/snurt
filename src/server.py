from sanic import Sanic, Blueprint
from decouple import config
from typing import cast

from .domain.auth.router import auth_router
from .middleware import error_handler
from .common import db

API_HOST = cast(str, config("API_HOST", default="0.0.0.0"))
API_PORT = cast(int, config("API_PORT", default=3333))
API_WORKERS = cast(int, config('API_WORKERS', default=1))
API_DEBUG = cast(bool, config('API_DEBUG', default=False))

app = Sanic(name="snurt")
app.error_handler.add(Exception, error_handler)

@app.before_server_start
async def initial_setup(self: Sanic):
    await db.connect()

@app.before_server_stop
async def clean_up(self: Sanic):
    await db.disconnect()

app.blueprint(Blueprint.group(auth_router, url_prefix="/api"))

if __name__ == "__main__":
    app.run(host=API_HOST, port=API_PORT, workers=API_WORKERS, debug=API_DEBUG)
