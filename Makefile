.PHONY: help setup clean test lint db-init db-migrate db-upgrade worker reset env

# Variables
# Shell to use with make
SHELL := /bin/bash

# Python and virtualenv
PYTHON := python
VENV := .venv
VENV_PYTHON := python
VENV_PIP := pip

VENV_ACTIVATE := $(VENV)/bin/activate
    RM := rm -rf
    MKDIR := mkdir -p
    CP := cp

# Flask & project settings
FLASK := flask
APP_NAME := run.py
PORT := 5000

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: $(VENV_ACTIVATE) .env db-init db-migrate db-upgrade ## Setup the project (venv, env vars, database)
	@echo "Setup complete!"

$(VENV_ACTIVATE):
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV)
	@$(VENV_PIP) install --upgrade pip
	@$(VENV_PIP) install -r requirements.txt
	@echo "Virtual environment created and dependencies installed."

.env: .env.example
	@if [ ! -f .env ]; then \
		echo "Creating .env file from example..."; \
		$(CP) .env.example .env; \
		echo ".env file created. You may want to edit it with your settings."; \
	else \
		echo ".env file already exists."; \
	fi

dev: ## Run the development server with debug mode enabled
	@echo "Starting Flask development server in debug mode..."
	@FLASK_ENV=development $(FLASK) run --host=0.0.0.0 --port=$(PORT) --debug


lint: ## Run linting checks
	@echo "Running linting checks..."
	@$(VENV_PYTHON) -m flake8

db-init: ## Initialize the database
	@echo "Initializing database..."
	@$(FLASK) db init

db-migrate: ## Generate a database migration
	@echo "Generating database migration..."
	@$(FLASK) db migrate -m "Migration $(shell date +%Y%m%d%H%M%S)"

db-upgrade: ## Apply database migrations
	@echo "Applying database migrations..."
	@$(FLASK) db upgrade

db-reset: clean-db db-init db-migrate db-upgrade ## Reset the database (WARNING: destroys all data)
	@echo "Database reset complete!"

clean-db: ## Remove the database files
	@echo "Removing database files..."
	@if [ -f app.db ]; then rm app.db; fi

shell: ## Start a Flask shell
	@echo "Starting Flask shell..."
	@$(FLASK) shell

routes: ## Show all registered routes
	@echo "Registered routes:"
	@$(FLASK) routes

clean: ## Clean up generated files and virtual environment
	@echo "Cleaning up..."
	@if [ -d "$(VENV)" ]; then $(RM) $(VENV); fi
	@if [ -d "__pycache__" ]; then $(RM) __pycache__; fi
	@if [ -d ".pytest_cache" ]; then $(RM) .pytest_cache; fi
	@find . -type d -name __pycache__ -exec $(RM) {} +
	@find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete!"