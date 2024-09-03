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
RUN echo $DB_NAME

# Define the command to run the Flask application using Gunicorn
# CMD ["gunicorn", "application:app", "-b", "0.0.0.0:5000", "-w", "4"]
CMD ["python", "main.py"]