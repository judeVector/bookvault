#!/bin/bash

# Start Django development server
python manage.py runserver 0.0.0.0:7000 &

# Start RabbitMQ consumers
python manage.py consume_borrow_messages &
python manage.py consume_user_messages &

# Wait indefinitely to keep the container alive
wait
