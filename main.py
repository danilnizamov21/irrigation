from fastapi import FastAPI

from api.auth import router as auth
from api.irigation import router as irrigation

app = FastAPI()

app.include_router(auth, prefix="/auth", tags=["Auth"])
app.include_router(irrigation, prefix="/irrigation", tags=["Irrigation"])
