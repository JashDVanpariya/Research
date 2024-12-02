# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to avoid prompts during package installs
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Run the application using Gunicorn (you can modify the number of workers as needed)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "demoproj.wsgi:application"]
