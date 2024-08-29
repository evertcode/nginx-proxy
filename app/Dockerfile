FROM python:3.9.19-alpine3.19

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./requirements.txt ./requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./app.py ./app.py

# Run app.py when the container launches
CMD ["python", "-u", "app.py"]
