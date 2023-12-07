FROM alpine

# Install dependencies
RUN apk update && \
    apk add --no-cache python3 py3-pip mariadb-connector-c-dev && \
    pip3 install --no-cache-dir pymysql cryptography==3.4.8 python-dotenv && \
    apk add --no-cache mariadb-client
    
# Copy source code to image
COPY ./app /app
# Set working directory
WORKDIR /app

# Run the application
CMD ["python3", "main.py"]