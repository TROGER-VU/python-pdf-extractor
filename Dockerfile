FROM python:3.10-slim

# Install system packages (Poppler + OCR deps)
RUN apt-get update && \
    apt-get install -y poppler-utils tesseract-ocr libgl1 libglib2.0-0 && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port 8501 for Streamlit
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
