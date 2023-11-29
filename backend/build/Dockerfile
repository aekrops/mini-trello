# Use an official Python runtime as a parent image
FROM python:3.10.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the backend directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run Django's development server when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
