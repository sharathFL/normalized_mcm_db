# Use official Python image from the Docker hub
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file (create one if you don't have it yet)
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script (create_db.py) into the container


# Set the command to run the Python script
CMD ["bash"]
