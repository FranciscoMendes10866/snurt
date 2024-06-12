from sanic import Blueprint

from .handlers import AuthHandlers

auth_router = Blueprint(name="auth_router", url_prefix="/auth")
handlers = AuthHandlers()

auth_router.add_route(handler=handlers.sign_in, uri="/sign-in", methods=["POST"])
