from config.settings import get_settings
from contextlib import asynccontextmanager
from apps.base.database import init_db
from fastapi import FastAPI


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    debug=settings.DEBUG,
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {"status": "ok", "message": "Application is healthy"}
