from fastapi import FastAPI
from pdf_service.src.pdf.router import router as pdf_router

app = FastAPI(
    title="PDF Service API",
)
app.include_router(pdf_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"status": "PDF Service is running"}
