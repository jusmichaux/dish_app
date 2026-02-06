#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run the Flet app on the port provided by Render
flet run main.py --web --port $PORT