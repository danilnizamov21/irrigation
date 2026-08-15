import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.admin import router as admin
from api.auth import router as auth
from api.esp import router as esp
from api.linking_module_to_user import router as linking

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger = logging.getLogger(__name__)


@app.middleware("http")
async def midleware_func(request: Request, call_next):

    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info(f"method={request.method}, url={request.url.path}, {process_time=}")

    return response


app.include_router(auth, prefix="/auth", tags=["Auth"])
app.include_router(esp, prefix="/irrigation", tags=["Irrigation"])
app.include_router(linking, prefix="/modules", tags=["Module"])
app.include_router(admin, prefix="/admin", tags=["Admin"])
