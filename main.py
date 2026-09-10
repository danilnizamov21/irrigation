import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.admin import router as admin
from api.auth import router as auth
from api.esp import router as esp
from api.linking_module_to_user import router as linking
from core.http_client import close_http_client, init_http_client
from core.redis_bd import close_redis, init_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await init_redis()
    app.state.http_client = await init_http_client()
    yield
    await close_http_client()
    await close_redis()


app = FastAPI(lifespan=lifespan)
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
