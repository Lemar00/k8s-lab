FROM python:3.9-alpine

WORKDIR /app

# Copy and install all the requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY app /app

# Expose port and run the app
EXPOSE 80
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "80"]
