from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


def generate_user_pdf(name: str, surname: str, email: str, date_of_birthday) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    content = [
        Paragraph("User Profile", styles["Title"]),
        Paragraph(f"Name: {name} {surname}", styles["Normal"]),
        Paragraph(f"Email: {email}", styles["Normal"]),
        Paragraph(f"Date of birth: {date_of_birthday}", styles["Normal"]),
    ]
    doc.build(content)
    buffer.seek(0)
    return buffer.getvalue()