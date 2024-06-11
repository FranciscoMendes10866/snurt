from sanic import Sanic, Blueprint
from prisma import Prisma

from .domain.auth.router import auth_router
from .common import AppContext, error_handler, AppInstance

app = Sanic(name="snurt", ctx=AppContext)
app.error_handler.add(Exception, error_handler)

@app.before_server_start
async def initial_setup(instance: AppInstance):
    db = Prisma()
    await db.connect()
    instance.ctx.db = db

@app.before_server_stop
async def clean_up(instance: AppInstance):
    await instance.ctx.db.disconnect()

app.blueprint(Blueprint.group(auth_router, url_prefix="/api"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3333, workers=1, debug=True)
