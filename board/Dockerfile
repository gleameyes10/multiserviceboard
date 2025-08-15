FROM python:3.11-slim

WORKDIR /app

# Install dependencies (including gunicorn)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Create SQLite data directory
RUN mkdir -p /app/data

# Copy application code
COPY . .

EXPOSE 5000

# Start with Gunicorn in production mode
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

