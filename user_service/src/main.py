import httpx
from fastapi import FastAPI, Depends, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from user_service.src.user.routers import router as auth_router

app = FastAPI(
    title="User Service API",
)
app.include_router(auth_router, prefix="/api/v1")


security = HTTPBearer()


@app.get(
    "/api/v1/pdf/profile",
    tags=["PDF"],
    summary="Download profile PDF",
    description="Generates and downloads a PDF with the current user's profile data.",
    response_class=Response,
    responses={200: {"content": {"application/pdf": {}}}},
)
async def pdf_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://pdf_service:8001/api/v1/pdf/profile",
            headers={"Authorization": f"Bearer {credentials.credentials}"},
        )
    return Response(
        content=response.content,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=profile.pdf"},
    )


@app.post(
    "/api/v1/pdf/save",
    tags=["PDF"],
    summary="Save PDF to S3 via SQS",
    description="Queues the user's profile PDF for saving to S3 via SQS.",
)
async def pdf_save(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://pdf_service:8001/api/v1/pdf/save",
            headers={"Authorization": f"Bearer {credentials.credentials}"},
        )
    return response.json()


@app.get("/")
def read_root():
    return {"status": "Backend is running"}

