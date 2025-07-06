#!/bin/bash

# Build script for Render.com deployment
echo "🚀 Starting Khalid Soft Student Management System deployment..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads
mkdir -p instance

echo "✅ Build completed successfully!"
echo "🎓 Khalid Soft Student Management System is ready!"
