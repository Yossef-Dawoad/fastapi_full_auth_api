from fastapi import FastAPI

from auth.user.routes import router as user_router

app = FastAPI()

app.include_router(user_router)




@app.get("/health-check")
def health_check() -> dict:
    return {"status": "ok"}
