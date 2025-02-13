# Use a Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt first to leverage Docker's caching mechanism
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Set the environment variable for Flask to run the app
ENV FLASK_APP=main
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Expose the port the app will run on
EXPOSE 5000

# Command to run the Flask app
CMD ["flask", "run"]
