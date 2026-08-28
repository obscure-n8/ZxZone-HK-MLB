#!/bin/bash

# ZxZone-HK-MLB Start Script for Heroku
echo "====================================="
echo "ZxZone-HK-MLB Bot Starting..."
echo "Powered By ZxZone Hub"
echo "====================================="

# Set environment
export PYTHONUNBUFFERED=1
export PORT=${PORT:-8080}

# Create necessary directories
mkdir -p /app/downloads /app/encode /app/thumbnails /app/config /app/sessions /app/data/logs

# Start Aria2 in background
if command -v aria2c &> /dev/null; then
    echo "Starting Aria2..."
    aria2c --enable-rpc \
        --rpc-listen-all=false \
        --rpc-allow-origin-all \
        --rpc-listen-port=6800 \
        --max-connection-per-server=8 \
        --split=8 \
        --dir=/app/downloads \
        --daemon=true \
        > /dev/null 2>&1 &
    echo "Aria2 started!"
fi

# Start web server in background
echo "Starting web server..."
python3 web_server.py > /dev/null 2>&1 &
WEB_PID=$!
echo "Web server started on port $PORT"

# Wait for web server
sleep 3

# Start main bot
echo "Starting Telegram Bot..."
python3 -m bot

# Keep container alive
echo "Bot exited, keeping web server alive..."
wait $WEB_PID
