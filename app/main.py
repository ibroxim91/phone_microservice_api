from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from app.routes import phone_router, auth_router
from fastapi.openapi.docs import get_redoc_html




@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(phone_router, prefix="/phone", tags=["phone"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
def hello_index():
    return {
        "message": "Hello index!",
    }




@app.get("/custom-redoc", include_in_schema=False)
async def custom_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Lead Service API",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js",
        redoc_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        with_google_fonts=True,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)