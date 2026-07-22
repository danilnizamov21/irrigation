from fastapi import FastAPI

from api.auth import router as auth

app = FastAPI()

app.include_router(auth, prefix="/auth", tags=["Auth"])
