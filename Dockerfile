# Start from an official, lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system-level build tools AND git
RUN apt-get update && apt-get install -y build-essential git

# Copy only the requirements file first to leverage Docker's caching
COPY requirements.txt .

# Install the Python dependencies with a 10-minute timeout
RUN pip install --no-cache-dir --timeout=600 -r requirements.txt

# --- NEW: Copy only the necessary files and folders ---
# Instead of 'COPY . .', we copy each part selectively.
COPY ./app ./app
COPY ./src ./src
COPY ./models ./models
COPY ./data/processed/final_features.csv ./data/processed/final_features.csv
COPY ./data/processed/labeled_features.csv ./data/processed/labeled_features.csv


# Tell Docker that the container will listen on port 8501
EXPOSE 8501

# The command to run when the container starts
CMD ["streamlit", "run", "app/dashboard.py"]