# Use a lightweight stable Python image
FROM python:3.11-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app.py .

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
