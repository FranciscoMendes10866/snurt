from sanic import HTTPResponse, SanicException, json

from ...common import BlueprintRequest, formatted_reply

class AuthHandlers:
    async def sign_in(self, request: BlueprintRequest) -> HTTPResponse:
        user = await request.app.ctx.db.user.find_first(where={"email": request.json["email"]})
        if not user:
            raise SanicException("User Not Found")
        else:
            return json(formatted_reply(datum=request.json))
