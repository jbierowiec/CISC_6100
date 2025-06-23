#!/bin/bash
# Start both Flask and Django servers properly

# Start Flask using gunicorn on Railway's required port 8080
cd frontend
gunicorn app:app --bind 0.0.0.0:8080 &
cd ..

# Optional: Start Django if needed on another port
cd backend
python manage.py runserver 0.0.0.0:8001
