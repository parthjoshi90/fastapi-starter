from config.settings import get_settings
from fastapi import FastAPI

settings = get_settings()

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)


@app.get("/health")
def health():
    return {"status": "ok", "message": "Application is healthy"}
