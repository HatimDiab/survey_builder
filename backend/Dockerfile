FROM python:3.12-slim AS base
RUN pip install --upgrade pip && pip install uv
WORKDIR /app
COPY requirements.txt .
RUN uv pip install --system --requirement requirements.txt
COPY . .
# Run migrations then launch API
CMD ["bash", "-c", "python scripts/migrate.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
