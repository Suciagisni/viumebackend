# Use an official Python runtime as a parent image
FROM python:3.8-slim


# Create and set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Gunicorn will listen on (usually 8000)
EXPOSE 8000

# Define the command to run your Flask application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
