from fastapi import FastAPI

from api.auth import router as auth
from api.esp import router as esp

app = FastAPI()

app.include_router(auth, prefix="/auth", tags=["Auth"])
app.include_router(esp, prefix="/irrigation", tags=["Irrigation"])
