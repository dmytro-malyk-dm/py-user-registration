FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app

WORKDIR /app

COPY pdf_service/requirements.txt ./pdf_service/requirements.txt
RUN pip install --no-cache-dir -r pdf_service/requirements.txt

COPY . .

CMD ["uvicorn", "pdf_service.src.main:app", "--host", "0.0.0.0", "--port", "8001"]