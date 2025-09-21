#!/bin/bash
# One-click start for Linux/Mac
cd "$(dirname "$0")"

# Check for Docker
if ! command -v docker &> /dev/null; then
	echo "Docker is not installed. Attempting to install Docker..."
	if [ "$(uname)" = "Linux" ]; then
		if [ -x "$(command -v apt-get)" ]; then
			sudo apt-get update
			sudo apt-get install -y docker.io
			sudo systemctl enable --now docker
		elif [ -x "$(command -v yum)" ]; then
			sudo yum install -y docker
			sudo systemctl enable --now docker
		else
			echo "Unsupported Linux distribution. Please install Docker manually."
			exit 1
		fi
	else
		echo "Please install Docker Desktop for Mac from https://www.docker.com/products/docker-desktop/"
		exit 1
	fi
fi

# Check for Docker Compose (plugin or legacy)
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
	echo "Docker Compose is not installed. Attempting to install Docker Compose..."
	if [ -x "$(command -v apt-get)" ]; then
		sudo apt-get update
		sudo apt-get install -y docker-compose
	elif [ -x "$(command -v yum)" ]; then
		sudo yum install -y docker-compose
	else
		echo "Unsupported Linux distribution. Please install Docker Compose manually."
		exit 1
	fi
fi

# Open browser
xdg-open http://localhost:8080 2>/dev/null || open http://localhost:8080 2>/dev/null &

# Use docker compose if available, else fallback to docker-compose
if docker compose version &> /dev/null; then
	docker compose up --build
else
	docker-compose up --build
fi
