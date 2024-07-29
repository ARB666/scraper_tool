# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements/base.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r base.txt

# Copy the rest of the application code into the container
COPY src /app/src

# Define a volume to mount a directory from the host machine
VOLUME /app/data

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
