from io import BytesIO
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from pdf_service.src.core.config import settings
from pdf_service.src.pdf.service import generate_user_pdf
from jose import jwt, JWTError

router = APIRouter(prefix="/pdf", tags=["PDF"])
security = HTTPBearer()


@router.get("/profile")
async def download_profile_pdf(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY_ACCESS,
            algorithms=[settings.JWT_SIGNING_ALGORITHM],
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    name = payload.get("name", "")
    surname = payload.get("surname", "")
    email = payload.get("email", "")
    date_of_birthday = payload.get("date_of_birthday", "")

    pdf_bytes = generate_user_pdf(
        name=name,
        surname=surname,
        email=email,
        date_of_birthday=date_of_birthday,
    )

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=profile.pdf"}
    )
