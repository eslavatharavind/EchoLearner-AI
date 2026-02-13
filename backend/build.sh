#!/bin/bash
# Render build script for installing system dependencies

echo "Installing system dependencies for PyMuPDF..."
apt-get update
apt-get install -y build-essential g++ libmupdf-dev mupdf-tools

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build completed successfully!"
