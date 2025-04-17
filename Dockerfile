# Use official Python 3.10 image as base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production
ENV DEBUG=False


# Set work directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    curl && \
    rm -rf /var/lib/apt/lists/*



# Install pipenv or use requirements.txt if you prefer
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files (optional: only for production)
RUN python manage.py collectstatic --noinput

# Run the application (override in docker-compose or CMD for dev)
CMD ["gunicorn", "backend_taxreminder.wsgi:application", "--bind", "0.0.0.0:8000"]
