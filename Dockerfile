# Start from an official, lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system-level build tools AND git
RUN apt-get update && apt-get install -y build-essential git

# Copy the requirements file into the container's working directory
COPY requirements.txt .

# --- FIX: Add a longer timeout for pip ---
# Install the Python dependencies with a 10-minute timeout
RUN pip install --no-cache-dir --timeout=600 -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Tell Docker that the container will listen on port 8501
EXPOSE 8501

# The command to run when the container starts
CMD ["streamlit", "run", "app/dashboard.py"]