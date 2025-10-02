#!/bin/bash

# Deployment script for the application
# Usage: ./deploy.sh <environment>

set -e  # Exit on any error

# Get deployment environment from argument
TARGET_ENV="${1:-staging}"
echo "Deploying to $TARGET_ENV environment..."

# Load environment variables if exists
if [ -f ".env.$TARGET_ENV" ]; then
    source ".env.$TARGET_ENV"
fi

# Validate required variables
if [ -z "$APP_ENV" ]; then
    echo "ERROR: APP_ENV not set"
    exit 1
fi

echo "Using APP_ENV=$APP_ENV"

# Deployment steps
echo "Step 1: Preparing deployment..."
sleep 2  # Simulate preparation

echo "Step 2: Validating configuration..."
sleep 1  # Simulate validation

echo "Step 3: Deploying application..."
sleep 2  # Simulate deployment

echo "Step 4: Running health checks..."
sleep 1  # Simulate health checks

echo "Deployment completed successfully!"
exit 0