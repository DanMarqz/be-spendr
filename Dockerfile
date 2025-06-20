FROM python:3.11.9-slim

# Set the working directory within the container
WORKDIR /spendr

# Copy the necessary files and directories into the container
COPY . .

# Upgrade pip and install Python dependencies
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask application
EXPOSE 5000
ARG DB_NAME
ARG PORT
ARG VERSION
ARG TOKEN
ARG APP_SECRET_KEY
ARG DB_URI
ARG DB_NAME
ARG ERROR_MSG
ARG DEBUG
RUN echo "DB_NAME=${DB_NAME}" > .env
RUN echo "PORT=${PORT}" >> .env
RUN echo "VERSION=${VERSION}" >> .env
RUN echo "TOKEN=${TOKEN}" >> .env
RUN echo "APP_SECRET_KEY=${APP_SECRET_KEY}" >> .env
RUN echo "DB_URI=${DB_URI}" >> .env
RUN echo "DB_NAME=${DB_NAME}" >> .env
RUN echo "ERROR_MSG=${ERROR_MSG}" >> .env
RUN echo "DEBUG=${DEBUG}" >> .env

# Define the command to run the Flask application using Gunicorn
CMD ["gunicorn", "main:create_app()", "-b", "0.0.0.0:5001", "-w", "1"]
# CMD ["python", "main.py"]