# Use an official Python runtime as a parent image
FROM python:3.15.0a2-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN apk add -u zlib-dev jpeg-dev gcc musl-dev
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Expose the port your app runs on
EXPOSE 5000


# Run the application
CMD ["python", "app.py"]