from fastapi import Depends, FastAPI
from pydantic import BaseModel
from api.irigation import router as send_values
app = FastAPI()

app.include_router(send_values, prefix="/values", tags=["Values"])