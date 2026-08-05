from fastapi import FastAPI

from api.auth import router as auth
from api.esp import router as esp
from api.linking_module_to_user import router as linking

app = FastAPI()

app.include_router(auth, prefix="/auth", tags=["Auth"])
app.include_router(esp, prefix="/irrigation", tags=["Irrigation"])
app.include_router(linking, prefix="/modules", tags=["Module"])
