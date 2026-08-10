import time

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

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


@app.middleware("http")
async def midleware_func(request: Request, call_next):
    if request.client.host == "127.0.0.1":
        return Response(status_code=429, content="вам запрещено делать запросы")
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    print(process_time)
    print(request.client.host)
    return response


app.include_router(auth, prefix="/auth", tags=["Auth"])
app.include_router(esp, prefix="/irrigation", tags=["Irrigation"])
app.include_router(linking, prefix="/modules", tags=["Module"])
