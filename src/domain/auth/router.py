from sanic import Blueprint,Request,HTTPResponse,json
from .handlers import AuthHandlers

auth_router = Blueprint(name="auth_router")
handlers = AuthHandlers()

auth_router.add_route(handler=handlers.sign_in, uri="/sign-in", methods=["POST"])
