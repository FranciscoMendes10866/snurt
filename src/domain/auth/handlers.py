from sanic import Request, HTTPResponse, SanicException, json

from ...common import formatted_reply
from .repo import AuthRepository

class AuthHandlers:
    __repo: AuthRepository

    def __init__(self):
        self.__repo = AuthRepository()

    async def sign_in(self, request: Request) -> HTTPResponse:
        user = await self.__repo.get_user_by_email(request.json["email"])
        if not user:
            raise SanicException("User Not Found")
        else:
            return json(formatted_reply(datum=request.json))
