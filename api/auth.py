from datetime import timedelta

from authx import AuthX, AuthXConfig, TokenPayload
from fastapi import APIRouter, Depends, Response

from schemas.user import UserLogin

router = APIRouter()
config = AuthXConfig()
config = AuthXConfig(
    JWT_SECRET_KEY="your-secret-keyq0w9odkq9e02di2093owdke9033iedo902de209",
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15),  # Short-lived
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30),  # Long-lived
)


auth = AuthX(config=config)
# Register error handlers for proper responses


@router.post("/login")
async def login(payload: UserLogin, responce: Response):
    pass


@router.post("/refresh")
async def refresh(payload: TokenPayload = Depends(auth.refresh_token_required)):
    """Exchange refresh token for new access token."""

    access_token = auth.create_access_token(uid=payload.sub)

    return {"access_token": access_token}


@router.get("/protected", dependencies=[Depends(auth.access_token_required)])
async def protected():
    return {"message": "Hello World"}
