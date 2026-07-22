from datetime import timedelta

from authx import AuthX, AuthXConfig, TokenPayload
from fastapi import APIRouter, Depends, HTTPException, Response

router = APIRouter()
config = AuthXConfig()
config = AuthXConfig(
    JWT_SECRET_KEY="your-secret-key",
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15),  # Short-lived
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30),  # Long-lived
)


auth = AuthX(config=config)
# Register error handlers for proper responses


@router.post("/login")
async def login(username: str, password: str, responce: Response):
    if username == "test" and password == "test":
        access_token = auth.create_access_token(uid=username)
        refresh_token = auth.create_refresh_token(uid=username)

        auth.set_refresh_cookies(refresh_token, responce, max_age=2592000)
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(401, detail="Invalid credentials")


@router.post("/refresh")
async def refresh(payload: TokenPayload = Depends(auth.refresh_token_required)):
    """Exchange refresh token for new access token."""

    access_token = auth.create_access_token(uid=payload.sub)

    return {"access_token": access_token}


@router.get("/protected", dependencies=[Depends(auth.access_token_required)])
async def protected():
    return {"message": "Hello World"}
