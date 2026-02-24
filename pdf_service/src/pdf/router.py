import base64
import json
from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from pdf_service.src.aws.clients import get_sqs_client, get_s3_client
from pdf_service.src.core.config import settings
from pdf_service.src.pdf.service import generate_user_pdf

router = APIRouter(prefix="/pdf", tags=["PDF"])
security = HTTPBearer()


def decode_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY_ACCESS,
            algorithms=[settings.JWT_SIGNING_ALGORITHM],
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


@router.get("/profile")
async def download_profile_pdf(payload: dict = Depends(decode_token)):
    pdf_bytes = generate_user_pdf(
        name=payload.get("name", ""),
        surname=payload.get("surname", ""),
        email=payload.get("email", ""),
        date_of_birthday=payload.get("date_of_birthday", ""),
    )
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=profile.pdf"},
    )


@router.post("/save", summary="Send PDF to S3 via SQS")
async def save_pdf_to_s3(payload: dict = Depends(decode_token)):
    user_id = payload.get("sub")
    s3_key = f"profiles/{user_id}.pdf"

    pdf_bytes = generate_user_pdf(
        name=payload.get("name", ""),
        surname=payload.get("surname", ""),
        email=payload.get("email", ""),
        date_of_birthday=payload.get("date_of_birthday", ""),
    )
    pdf_b64 = base64.b64encode(pdf_bytes).decode()

    sqs = get_sqs_client()
    sqs.send_message(
        QueueUrl=settings.SQS_QUEUE_URL,
        MessageBody=json.dumps({
            "user_id": user_id,
            "email": payload.get("email"),
            "pdf": pdf_b64,
        }),
    )

    s3 = get_s3_client()
    presigned_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.S3_BUCKET_NAME, "Key": s3_key},
        ExpiresIn=3600,
    )

    return {
        "detail": "PDF queued for saving to S3",
        "s3_url": presigned_url,
    }
