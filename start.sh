#!/bin/bash

# Kill existing processes using these ports
lsof -ti tcp:8060 | xargs kill -9 2>/dev/null
lsof -ti tcp:8000 | xargs kill -9 2>/dev/null

# Start Flask frontend on port 8060 in background
cd frontend
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=8060 &
cd ..

# Start Django
cd backend
python manage.py runserver 0.0.0.0:8000
