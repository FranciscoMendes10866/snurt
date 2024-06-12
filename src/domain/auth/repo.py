from prisma import Prisma

from ...common import db

class AuthRepository:
    async def get_user_by_email(self, email: str):
        return await db.user.find_first(where={"email": email})
