#!/bin/bash
#ehh kinda works
# Move into Flask Python server directory
cd /WebApplication/backend

# Activate virtual environment if necessary
# source /path/to/virtualenv/bin/activate
source venv/bin/activate
# Start Flask server
python app.py 

# Move into React frontend directory
cd WebApplication/frontend/apws

# Install dependencies if necessary
# npm install

# Start React frontend
npm start
