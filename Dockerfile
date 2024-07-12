# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y libgomp1 libgl1 libsm6 libxext6 libxrender-dev libglib2.0-0

# Install additional packages required for your project
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI and Streamlit application files into the container
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Expose the Streamlit port
EXPOSE 8501

# Command to run both FastAPI and Streamlit
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run frontend.py"]