# STAGE 1: Build Stage
FROM python:3.13-slim AS builder

# Install system dependencies
RUN apt-get update &&  apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

# Copy application code
COPY . .

# STAGE 2: Runtime Stage
FROM python:3.13-slim AS runtime

# Create a non-root user
RUN useradd --create-home appUser

# Create app directory and assign ownership
RUN mkdir -p /home/appUser/app && chown -R appUser:appUser /home/appUser/app

# Copy installed dependencies and application code from the builder stage
COPY --from=builder /app /home/appUser/app
COPY --from=builder /root/.local /home/appUser/.local

# Set environment variables
ENV PATH="/home/appUser/.local/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Fix permissions for .local
RUN chown -R appUser:appUser /home/appUser/.local

# Switch to non-root user and set working directory
USER appUser
WORKDIR /home/appUser/app

# Expose port and run the application
EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]
