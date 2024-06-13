from sanic import Request, HTTPResponse, json, SanicException

from ...common import formatted_reply, hash_password, create_session, sign_jwt, verify_password, verify_session
from .repo import AuthRepository
from ...middleware import authorized, ContextAwareRequest

class AuthHandlers:
    __repo: AuthRepository

    def __init__(self):
        self.__repo = AuthRepository()

    async def sign_up(self, request: Request) -> HTTPResponse:
        email = request.json["email"]
        password = request.json["password"]
        if not email or not password:
            raise SanicException(message="Email and Password are required fields", status_code=400)

        user = await self.__repo.get_user_by_email(email)
        if user:
            raise SanicException(message="Email already taken", status_code=400)

        hashed_password = hash_password(password)
        user_record = await self.__repo.insert_user(email=email, password=hashed_password)

        access_token = sign_jwt(user_record.id)
        if not access_token:
            raise SanicException()

        expires_at = create_session()
        user_session = await self.__repo.create_new_session(expires_at, user_record.id)

        return json(
            formatted_reply(datum={"access_token": access_token, "session": user_session.id})
        )


    async def sign_in(self, request: Request) -> HTTPResponse:
        email = request.json["email"]
        password = request.json["password"]
        if not email or not password:
            raise SanicException(message="Email and Password are required fields", status_code=400)

        user = await self.__repo.get_user_by_email(email)
        if not user:
            raise SanicException(message="User does not exist", status_code=404)

        is_valid = verify_password(text=password, hashed=user.password)
        if not is_valid:
            raise SanicException(message="Invalid credentials", status_code=400)

        access_token = sign_jwt(user.id)
        if not access_token:
            raise SanicException()

        expires_at = create_session()
        user_session = await self.__repo.create_new_session(expires_at, user.id)

        return json(
            formatted_reply(datum={"access_token": access_token, "session": user_session.id})
        )

    async def renew_session(self, request: Request) -> HTTPResponse:
        session_id = request.json["sessionId"]
        if not session_id:
            raise SanicException(message="Missing required fields", status_code=400)

        session = await self.__repo.get_session_by_id(session_id)
        if not session:
            raise SanicException(message="Unauthorized", status_code=401)

        await self.__repo.delete_session_by_id(session_id)

        is_expired = verify_session(session.expires_at)
        if is_expired:
            raise SanicException(message="Forbidden", status_code=403)

        access_token = sign_jwt(session.user_id)
        if not access_token:
            raise SanicException()

        expires_at = create_session()
        user_session = await self.__repo.create_new_session(expires_at, session.user_id)

        return json(
            formatted_reply(datum={"access_token": access_token, "session": user_session.id})
        )

    @authorized()
    async def sign_out(self, request: ContextAwareRequest) -> HTTPResponse:
        session_id = request.json["sessionId"]
        if not session_id:
            raise SanicException(message="Missing required fields", status_code=400)

        session = await self.__repo.get_session_by_id(session_id)
        if not session:
            raise SanicException(message="Forbidden", status_code=403)

        if session.user_id != request.ctx.user_id:
            raise SanicException(message="Forbidden", status_code=403)

        await self.__repo.delete_session_by_id(session_id)

        return json(formatted_reply())
