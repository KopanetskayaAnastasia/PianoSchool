# Use the official Python image from the Docker Hub
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY . .

WORKDIR /app/pianoschool

RUN python manage.py migrate --noinput
RUN python manage.py createsu
RUN python manage.py collectstatic --noinput

# Run the Django development server
CMD gunicorn pianoschool.wsgi:application --bind 0.0.0.0:$PORT