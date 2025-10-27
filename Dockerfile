# Use the official Python image from the Docker Hub
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY . /app/

ENV DJANGO_SETTINGS_MODULE=pianoschool.pianoschool.settings

RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

# Expose the port that the app runs on
EXPOSE 10000

# Run the Django development server
CMD ["gunicorn", "pianoschool.pianoschool.wsgi:application", "--bind", "0.0.0.0:10000"]