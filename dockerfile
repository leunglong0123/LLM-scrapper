# Use the official Python image as a base
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the current directory into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 8080

# Set the entrypoint to run the app
CMD ["python", "app.py"]
