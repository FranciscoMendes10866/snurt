from sanic import Request, HTTPResponse, BadRequest, ServerError, Unauthorized, Forbidden, json

from ...common import formatted_reply, hash_password, create_session, sign_jwt, verify_password, verify_session
from .repo import AuthRepository

class AuthHandlers:
    __repo: AuthRepository

    def __init__(self):
        self.__repo = AuthRepository()

    async def sign_up(self, request: Request) -> HTTPResponse:
        email = request.json["email"]
        password = request.json["password"]
        if not email or not password:
            raise BadRequest("Email and Password are required fields")

        user = await self.__repo.get_user_by_email(email)
        if user:
            raise ServerError("Email already taken")

        hashed_password = hash_password(password)
        user_record = await self.__repo.insert_user(email=email, password=hashed_password)

        expires_at = create_session()
        user_session = await self.__repo.create_new_session(expires_at, user_record.id)
        access_token = sign_jwt(user_record.id)

        return json(
            formatted_reply(datum={"session": user_session.id, "access_token": access_token})
        )


    async def sign_in(self, request: Request) -> HTTPResponse:
        email = request.json["email"]
        password = request.json["password"]
        if not email or not password:
            raise BadRequest("Email and Password are required fields")

        user = await self.__repo.get_user_by_email(email)
        if not user:
            raise ServerError("User does not exist")

        is_valid = verify_password(text=password, hashed=user.password)
        if not is_valid:
            raise ServerError("Invalid credentials")

        expires_at = create_session()
        user_session = await self.__repo.create_new_session(expires_at, user.id)
        access_token = sign_jwt(user.id)

        return json(
            formatted_reply(datum={"session": user_session.id, "access_token": access_token})
        )

    async def renew_session(self, request: Request) -> HTTPResponse:
        session_id = request.json["sessionId"]
        if not session_id:
            raise BadRequest()

        session = await self.__repo.get_session_by_id(session_id)
        if not session:
            raise Unauthorized()

        await self.__repo.delete_session_by_id(session_id)

        is_expired = verify_session(session.expires_at)
        if is_expired:
            raise Forbidden()

        expires_at = create_session()
        user_session = await self.__repo.create_new_session(expires_at, session.user_id)
        access_token = sign_jwt(session.user_id)

        return json(
            formatted_reply(datum={"session": user_session.id, "access_token": access_token})
        )

    async def sign_out(self, request: Request) -> HTTPResponse:
        session_id = request.json["sessionId"]
        if not session_id:
            raise BadRequest()

        # TODO: protect route and make sure that only the session owner can delete it
        await self.__repo.delete_session_by_id(session_id)

        return json(formatted_reply())
