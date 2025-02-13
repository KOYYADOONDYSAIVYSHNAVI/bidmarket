# Use the official Python image as a base
FROM python:3.9-slim

# Set a working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the application
CMD ["python", "main.py"]
