# Dockerfile for Order Service
FROM python:3.9-slim

RUN pip install flask requests kafka-python

WORKDIR /app

COPY order_service.py /app/

CMD ["python", "order_service.py"]

# Dockerfile for Payment Service
FROM python:3.9-slim

RUN pip install flask kafka-python

WORKDIR /app

COPY payment_service.py /app/

CMD ["python", "payment_service.py"]

# Dockerfile for Stock Service
FROM python:3.9-slim

RUN pip install flask kafka-python

WORKDIR /app

COPY stock_service.py /app/

CMD ["python", "stock_service.py"]

# Dockerfile for Notification Service
FROM python:3.9-slim

RUN pip install flask kafka-python

WORKDIR /app

COPY notification_service.py /app/

CMD ["python", "notification_service.py"]

# Dockerfile for User Service
FROM python:3.9-slim

RUN pip install flask kafka-python

WORKDIR /app

COPY user_service.py /app/

CMD ["python", "user_service.py"]

# Dockerfile for Python API Gateway
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY app/ .

# Expose the port
EXPOSE 5000

# Command to run the app
CMD ["python", "api_gateway.py"]
