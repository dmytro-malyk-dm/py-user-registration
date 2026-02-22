from fastapi import FastAPI
from src.routers.user import router as auth_router

app = FastAPI(title="User registration API", debug=True)
app.include_router(auth_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"status": "Backend is running"}

