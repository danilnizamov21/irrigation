from user import UserLogin

from api import auth


class Tokens:
    async def login(self, payload: UserLogin):
        if payload.login == "test" and payload.password == "test12345678":
            access_token = auth.create_access_token(uid=payload.login)
            refresh_token = auth.create_refresh_token(uid=payload.login)

            auth.set_refresh_cookies(refresh_token, responce, max_age=2592000)
            return {"access_token": access_token, "token_type": "bearer"}
        raise HTTPException(401, detail="Invalid credentials")
