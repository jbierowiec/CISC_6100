#!/bin/bash
# Start both Flask and Django servers in the background

# Start Flask (now using port 5050)
cd frontend
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=8025 &
cd ..

# Start Django
cd backend
python manage.py runserver 0.0.0.0:8000
