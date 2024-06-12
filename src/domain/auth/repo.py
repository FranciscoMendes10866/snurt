from prisma import Prisma

from ...common import db

class AuthRepository:
    async def get_user_by_email(self, email: str):
        return await db.user.find_first(where={"email": email})

    async def insert_user(self, email: str, password: str):
        return await db.user.create({"email": email, "password": password})

    async def create_new_session(self, expires_at: float, user_id: int):
        return await db.sessions.create({"expires_at": expires_at, "user_id": user_id})

    async def get_session_by_id(self, session_id: int):
        return await db.sessions.find_first(where={"id": session_id})

    async def delete_session_by_id(self, session_id: int):
        return await db.sessions.delete(where={"id": session_id})
