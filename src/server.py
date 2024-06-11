from sanic import Sanic,Request,HTTPResponse,json
from .domain.auth.router import auth_router

app = Sanic(name="learn_sanic")

app.blueprint(blueprint=auth_router, url_prefix="auth")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3333, workers=2, debug=True)
