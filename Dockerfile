# --- Backend Stage ---
FROM python:3.11-slim AS backend

WORKDIR /app/backend

# Install Poetry and system dependencies
RUN pip install --upgrade pip && \
    pip install poetry

COPY backend/pyproject.toml backend/poetry.lock* ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY backend/ .

# --- Frontend Stage ---
FROM node:20 AS frontend

WORKDIR /app/frontend

COPY frontend/shp-learners/package*.json ./
RUN npm install

COPY frontend/shp-learners/ ./
RUN npm run build

# --- Final Stage ---
FROM python:3.11-slim

WORKDIR /app

# Copy backend code and dependencies
COPY --from=backend /app/backend /app/backend

# Copy frontend build to backend staticfiles (adjust path as needed)
COPY --from=frontend /app/frontend/dist /app/backend/static/

# Install Poetry and dependencies
RUN pip install --upgrade pip && \
    pip install poetry && \
    cd backend && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Expose port (adjust if needed)
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Start Django server (adjust if using gunicorn/uvicorn)
CMD ["sh", "-c", "cd backend && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
