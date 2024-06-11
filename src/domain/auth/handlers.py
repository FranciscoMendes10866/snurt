from sanic import HTTPResponse, SanicException, json

from ...common import BlueprintRequest

class AuthHandlers:
    async def sign_in(self, request: BlueprintRequest) -> HTTPResponse:
        user = await request.app.ctx.db.user.find_first(where={"email": request.json["email"]})
        if not user:
            raise SanicException("User Not Found")
        else:
            return json(request.json)
