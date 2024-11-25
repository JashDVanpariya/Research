# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . /app/

# Expose the port that your app runs on
EXPOSE 8000

# Command to run the application with gunicorn for production
CMD ["gunicorn", "demoproj.wsgi:application", "--workers", "3", "--bind", "0.0.0.0:8000"]