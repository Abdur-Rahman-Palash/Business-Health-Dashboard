# Executive Dashboard - Dockerfile for Streamlit
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements-streamlit.txt .
RUN pip install --no-cache-dir -r requirements-streamlit.txt

# Copy Streamlit app
COPY backend/ ./backend/

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "backend/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
