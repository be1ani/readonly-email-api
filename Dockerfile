FROM python:3.12-slim

WORKDIR /app

COPY fetch_emails.py .

RUN pip install --no-cache-dir python-dotenv

CMD ["python", "fetch_emails.py"]
