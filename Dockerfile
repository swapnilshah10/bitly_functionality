# Step 1: Use the official Python base image
FROM python:3.11-slim

# Step 2: Set environment variables to avoid Python writing .pyc files to the container and buffering output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Step 3: Set the working directory in the container
WORKDIR /app

# Step 4: Install system dependencies (e.g., for PostgreSQL or other DB connectors)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Install pipenv or pip to manage dependencies
COPY requirements.txt /app/


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the Django project files into the container
COPY . /app/

WORKDIR /app/bitly_clone/
# Step 7: Expose port 8000 for the Django app
EXPOSE 8000

# Step 8: Run migrations and start the application
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
