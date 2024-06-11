from sanic import Request,HTTPResponse,json

class AuthHandlers:
    async def sign_in(self, request: Request) -> HTTPResponse:
        return json(request.json)
