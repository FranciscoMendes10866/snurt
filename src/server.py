from sanic import Sanic, Blueprint
from prisma import Prisma

from .domain.auth.router import auth_router
from .common import error_handler, db

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
    app.run(host="0.0.0.0", port=3333, workers=1, debug=True)
