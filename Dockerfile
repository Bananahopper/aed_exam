# Use Python 3.11 slim image for better compatibility
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Create necessary directories
RUN mkdir -p data/raw data/processed data/results outputs/charts outputs/tables

# Set environment variables
ENV PYTHONPATH=/app
ENV JUPYTER_ENABLE_LAB=yes

# Expose Jupyter port
EXPOSE 8888

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "🚀 Starting Risk Analysis Environment..."\n\
echo "📊 Project structure:"\n\
ls -la\n\
echo "\n📁 Data directories:"\n\
ls -la data/\n\
echo "\n🔧 Available commands:"\n\
echo "  • jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root"\n\
echo "  • python risk_analysis_script.py"\n\
echo "  • python -m src.main"\n\
echo "\n💡 Access Jupyter at: http://localhost:8888"\n\
echo "🔑 Jupyter token will be shown below:"\n\
echo ""\n\
exec "$@"' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Default command - run main.py
CMD ["/app/entrypoint.sh", "python", "main.py"]