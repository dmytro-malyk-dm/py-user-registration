FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app

WORKDIR /app

COPY user_service/requirements.txt ./user_service/requirements.txt

RUN pip install --no-cache-dir -r user_service/requirements.txt

COPY . .

CMD ["uvicorn", "pdf_service.src.main:app", "--host", "0.0.0.0", "--port", "8001"]