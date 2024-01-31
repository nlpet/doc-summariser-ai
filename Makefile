# Makefile for managing a FastAPI application

# Variables
PYTHON=python3
PIP=pip3
SERVER=uvicorn
APP_MODULE=api.main:app
HOST=0.0.0.0
PORT=8000
RELOAD=--reload

.PHONY: all install run test

all: install

# Install dependencies
install:
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

# Run the FastAPI server with hot reload for development
run:
	$(SERVER) $(APP_MODULE) --host $(HOST) --port $(PORT) $(RELOAD)

docker-run:
	docker build -t summarise-api .
	docker run -d --name summarise-api -p 80:80 summarise-api

docker-clean:
	docker stop summarise-api
	docker rm summarise-api

# Run tests (replace 'pytest' with your test runner if different)
test:
	pytest -v

