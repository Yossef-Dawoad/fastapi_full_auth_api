from fastapi import FastAPI

from auth.user.routes import router as user_router

app = FastAPI(
    title="Auth API",
    docs_url="/",
    description="Authentication API",
    version="0.1.0",
    openapi_tags=[
        {
            "name": "Users",
            "description": "Operations with users",
        },
    ],
)

app.include_router(user_router)




@app.get("/health-check")
def health_check() -> dict:
    return {"status": "ok"}
