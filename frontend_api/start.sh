#!/bin/bash

# Make Migrations
python manage.py makemigrations &
python manage.py migrate &

# Start Django development server
python manage.py runserver 0.0.0.0:8000 &

# Start RabbitMQ consumer
python manage.py consume_rabbit &

# Wait indefinitely to keep the container alive
wait
