# Use an official Python runtime as a parent image

FROM python:3.10-slim



# Set the working directory in the container

WORKDIR /app



# Install system dependencies (build tools often needed for some python packages)

RUN apt-get update && apt-get install -y --no-install-recommends \

    build-essential \

    && rm -rf /var/lib/apt/lists/*



# Copy requirements first to leverage Docker cache

COPY requirements.txt .



# Install Python dependencies

RUN pip install --no-cache-dir -r requirements.txt



# Copy the rest of the application code

COPY . .



# Expose ports for Streamlit (8501) and FastAPI (8000)

EXPOSE 8501

EXPOSE 8000



# By default, we will run a script that starts both, 

# or we can override this in docker-compose.


