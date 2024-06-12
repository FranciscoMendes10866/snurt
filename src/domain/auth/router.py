from sanic import Blueprint

from .handlers import AuthHandlers

auth_router = Blueprint(name="auth_router", url_prefix="/auth")
handlers = AuthHandlers()

auth_router.add_route(handler=handlers.sign_up, uri="/sign-up", methods=["POST"])
auth_router.add_route(handler=handlers.sign_in, uri="/sign-in", methods=["POST"])
auth_router.add_route(handler=handlers.renew_session, uri="/renew-session", methods=["POST"])
auth_router.add_route(handler=handlers.sign_out, uri="/sign-out", methods=["POST"])
